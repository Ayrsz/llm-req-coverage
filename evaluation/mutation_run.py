#!/usr/bin/env python3
"""Avaliação por mutação automática (mutmut) da suíte gerada pelo LLM.

Para cada ``(requisito, estratégia)``, usa a suíte de testes gerada como conjunto
de testes e roda o ``mutmut`` sobre a implementação correta (montada como
``solution.py`` num diretório isolado), coletando mutantes mortos e sobreviventes.

Camadas (a fronteira de teste é o *parsing*, ver ``tests/test_mutation_run.py``):

- **pura** (sem I/O, testável offline): ``parse_run_total``, ``parse_results``,
  ``build_mutation_result``, ``mutation_score``;
- **invocação** (I/O, chama o ``mutmut`` real): ``prepare_workdir``,
  ``run_mutmut``, ``show_survivor_diff`` — adicionadas nas tarefas T09/T10;
- **orquestração**: ``evaluate_config`` / ``main`` — T11/T12.

Este módulo NÃO importa ``llm_client`` nem nada que toque a API, para que o teste
offline (CA4) possa importá-lo sem efeitos colaterais.
"""

from __future__ import annotations

import csv
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = REPO_ROOT / "evaluation" / "results_matrix.csv"
DEFAULT_GENERATED = REPO_ROOT / "generated_tests"
DEFAULT_IMPL = REPO_ROOT / "implementations"

STRATEGIES = ("direct", "two_step")

# Linha-resumo da matriz que não corresponde a um node id de teste real.
COLLECTION_ERROR = "<collection_error>"

# Status que o ``mutmut results`` lista (todos significam "não-morto").
NOT_KILLED_STATUSES = ("survived", "timeout", "suspicious", "skipped")


@dataclass
class MutationResult:
    """Resultado de mutação de uma config, já agregado.

    ``killed`` é derivado: ``total`` menos tudo o que o ``mutmut results`` lista
    (que é, por definição, o conjunto de não-mortos).
    """

    total: int
    killed: int
    survived: list[str] = field(default_factory=list)
    timeout: list[str] = field(default_factory=list)
    suspicious: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


_PROGRESS_RE = re.compile(r"(\d+)/(\d+)")
_RESULT_LINE_RE = re.compile(
    r"^\s*(solution\.\S+__mutmut_\d+):\s*(\w+)\s*$"
)


def parse_run_total(run_stdout: str) -> int:
    """Extrai o total de mutantes da linha-resumo do ``mutmut run``.

    A linha-resumo final tem o formato ``… N/N  🎉 K 🫥 …`` (com spinners e
    emojis no entorno). Retorna o segundo grupo do ÚLTIMO ``(\\d+)/(\\d+)``.
    """
    matches = _PROGRESS_RE.findall(run_stdout)
    if not matches:
        raise ValueError(
            "Não foi possível extrair o total de mutantes da saída do "
            "'mutmut run' (nenhuma ocorrência de N/N encontrada)."
        )
    return int(matches[-1][1])


def parse_results(results_stdout: str) -> dict[str, list[str]]:
    """Parseia a saída do ``mutmut results`` (lista só os não-mortos).

    Cada linha relevante tem o formato
    ``    solution.<nome>__mutmut_<N>: <status>``. Devolve ``{status: [ids]}``.
    Ignora ruído (warnings, linhas em branco).
    """
    by_status: dict[str, list[str]] = {}
    for line in results_stdout.splitlines():
        m = _RESULT_LINE_RE.match(line)
        if not m:
            continue
        mutant_id, status = m.group(1), m.group(2)
        by_status.setdefault(status, []).append(mutant_id)
    return by_status


def build_mutation_result(total: int, results_by_status: dict[str, list[str]]) -> MutationResult:
    """Monta o ``MutationResult`` a partir do total e dos não-mortos.

    Convenção: ``killed = total − (nº de mutantes listados pelo results)``.
    """
    not_killed = sum(len(results_by_status.get(s, [])) for s in NOT_KILLED_STATUSES)
    return MutationResult(
        total=total,
        killed=total - not_killed,
        survived=list(results_by_status.get("survived", [])),
        timeout=list(results_by_status.get("timeout", [])),
        suspicious=list(results_by_status.get("suspicious", [])),
        skipped=list(results_by_status.get("skipped", [])),
    )


def mutation_score(result: MutationResult) -> float:
    """``killed / total``, arredondado a 4 casas; ``0.0`` se ``total == 0``."""
    if result.total == 0:
        return 0.0
    return round(result.killed / result.total, 4)


# --- Filtro de baseline verde (T07/T08) -----------------------------------
# O ``mutmut`` exige que a suíte passe inteira na implementação não-mutada; um
# teste ``invalid`` (que reprova na ``correct.py``) faz o ``mutmut`` abortar.
# A classificação por teste já existe em ``results_matrix.csv``; reusamos.


def _config_rows(req_id: str, strategy: str, matrix_path) -> list[dict]:
    with open(matrix_path, newline="", encoding="utf-8") as f:
        return [
            row for row in csv.DictReader(f)
            if row["requirement"] == req_id and row["strategy"] == strategy
        ]


def select_passing_tests(req_id: str, strategy: str, matrix_path=DEFAULT_MATRIX) -> list[str]:
    """Nomes de teste que passam na implementação correta (``correct == pass``)."""
    return [r["test"] for r in _config_rows(req_id, strategy, matrix_path)
            if r["correct"] == "pass"]


def select_failing_tests(req_id: str, strategy: str, matrix_path=DEFAULT_MATRIX) -> list[str]:
    """Nomes de teste a deselecionar: reprovam na correta (``correct != pass``).

    Exclui a linha-resumo ``<collection_error>``, que não é um node id real.
    """
    return [r["test"] for r in _config_rows(req_id, strategy, matrix_path)
            if r["correct"] != "pass" and r["test"] != COLLECTION_ERROR]


def should_skip(passing_tests: list[str]) -> bool:
    """Decide se a config deve ser ``skipped``: sem nenhum teste verde."""
    return not passing_tests


# --- Camada de invocação (I/O; chama o mutmut real) -----------------------
# Mesma ideia de isolamento de run_tests.py::run_against_variant: a variante vira
# solution.py num diretório próprio e o teste é copiado para lá. Diferença: o
# diretório PRECISA persistir entre 'mutmut run', 'results' e 'show', então o
# chamador é responsável por removê-lo (não usamos TemporaryDirectory aqui).


def _setup_cfg(deselect_node_ids: list[str]) -> str:
    """Conteúdo do setup.cfg do workdir.

    ``source_paths=solution.py`` (NÃO ``paths_to_mutate``, deprecado no 3.6.0).
    Os reprovados na correta entram como pares ``--deselect <node id>`` em
    ``pytest_add_cli_args`` (um argumento por linha), garantindo baseline verde:
    sem isso o mutmut aborta com ``failed to collect stats``.
    """
    lines = ["[mutmut]", "source_paths=solution.py"]
    if deselect_node_ids:
        lines.append("pytest_add_cli_args=")
        for nid in deselect_node_ids:
            lines.append("    --deselect")
            lines.append(f"    {nid}")
    return "\n".join(lines) + "\n"


def prepare_workdir(req_id: str, strategy: str, failing_tests: list[str], *,
                    generated_dir=DEFAULT_GENERATED, impl_dir=DEFAULT_IMPL) -> Path:
    """Monta um diretório isolado para o mutmut e devolve seu caminho.

    Copia ``correct.py`` → ``solution.py`` e o teste gerado → ``test_generated.py``;
    escreve ``setup.cfg`` deselecionando ``failing_tests`` (node ids). O chamador
    deve remover o diretório ao terminar.
    """
    workdir = Path(tempfile.mkdtemp(prefix=f"mutmut_{req_id}_{strategy}_"))
    shutil.copyfile(impl_dir / req_id / "correct.py", workdir / "solution.py")
    shutil.copyfile(generated_dir / strategy / f"test_{req_id}.py",
                    workdir / "test_generated.py")
    node_ids = [f"test_generated.py::{t}" for t in failing_tests]
    (workdir / "setup.cfg").write_text(_setup_cfg(node_ids), encoding="utf-8")
    return workdir


def run_mutmut(workdir: Path, timeout: int) -> tuple[str, str]:
    """Roda ``mutmut run`` e depois ``mutmut results`` com cwd no ``workdir``.

    Usa ``sys.executable -m mutmut`` (o binário do PATH pode apontar para outro
    interpretador). ``results`` é chamado SEM ``--all`` — com ``--all`` os mortos
    também seriam listados e a convenção de score (killed = total − listados)
    ficaria incorreta. Devolve ``(run_stdout, results_stdout)``.
    """
    run = subprocess.run(
        [sys.executable, "-m", "mutmut", "run"],
        cwd=workdir, timeout=timeout, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    results = subprocess.run(
        [sys.executable, "-m", "mutmut", "results"],
        cwd=workdir, timeout=timeout, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    return run.stdout, results.stdout


def show_survivor_diff(workdir: Path, mutant_id: str) -> str:
    """Diff de um mutante via ``mutmut show <id>`` (cwd no workdir)."""
    r = subprocess.run(
        [sys.executable, "-m", "mutmut", "show", mutant_id],
        cwd=workdir, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    return r.stdout


# --- Montagem de linhas de CSV (puro) -------------------------------------

SUMMARY_FIELDS = [
    "requirement", "strategy", "mutants_total", "mutants_killed",
    "mutants_survived", "mutants_timeout", "mutants_suspicious",
    "mutation_score_auto", "status",
]
SURVIVOR_FIELDS = ["requirement", "strategy", "mutant_id", "status", "diff"]


def summary_row(req_id: str, strategy: str, status: str,
                result: MutationResult | None = None) -> dict:
    """Uma linha de ``mutation_summary.csv``. ``result=None`` ⇒ config sem dados."""
    if result is None:
        return {
            "requirement": req_id, "strategy": strategy,
            "mutants_total": 0, "mutants_killed": 0, "mutants_survived": 0,
            "mutants_timeout": 0, "mutants_suspicious": 0,
            "mutation_score_auto": 0.0, "status": status,
        }
    return {
        "requirement": req_id, "strategy": strategy,
        "mutants_total": result.total, "mutants_killed": result.killed,
        "mutants_survived": len(result.survived),
        "mutants_timeout": len(result.timeout),
        "mutants_suspicious": len(result.suspicious),
        "mutation_score_auto": mutation_score(result), "status": status,
    }


def survivor_rows(req_id: str, strategy: str, result: MutationResult,
                  diffs: dict[str, str]) -> list[dict]:
    """Linhas de ``mutation_survivors.csv``: um mutante não-morto por linha."""
    rows = []
    for status_name in NOT_KILLED_STATUSES:
        for mutant_id in getattr(result, status_name):
            rows.append({
                "requirement": req_id, "strategy": strategy,
                "mutant_id": mutant_id, "status": status_name,
                "diff": diffs.get(mutant_id, ""),
            })
    return rows


# --- Orquestração ---------------------------------------------------------


def evaluate_config(req_id: str, strategy: str, *, timeout: int = 120,
                    matrix_path=DEFAULT_MATRIX, generated_dir=DEFAULT_GENERATED,
                    impl_dir=DEFAULT_IMPL) -> tuple[dict, list[dict]]:
    """Avalia uma ``(requisito, estratégia)``: invocação → parsing → linhas.

    Devolve ``(linha_summary, linhas_survivors)``. Config sem testes verdes é
    ``skipped`` sem invocar o mutmut. Falha de execução vira ``status="error"``.
    """
    passing = select_passing_tests(req_id, strategy, matrix_path)
    if should_skip(passing):
        return summary_row(req_id, strategy, "skipped"), []

    failing = select_failing_tests(req_id, strategy, matrix_path)
    workdir = prepare_workdir(req_id, strategy, failing,
                              generated_dir=generated_dir, impl_dir=impl_dir)
    try:
        run_out, results_out = run_mutmut(workdir, timeout)
        total = parse_run_total(run_out)
        result = build_mutation_result(total, parse_results(results_out))
        diffs = {
            mid: show_survivor_diff(workdir, mid)
            for status_name in NOT_KILLED_STATUSES
            for mid in getattr(result, status_name)
        }
        return (summary_row(req_id, strategy, "ok", result),
                survivor_rows(req_id, strategy, result, diffs))
    except (subprocess.TimeoutExpired, ValueError) as exc:
        print(f"  [erro] {req_id}/{strategy}: {type(exc).__name__}", file=sys.stderr)
        return summary_row(req_id, strategy, "error"), []
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        # lineterminator="\n": fins de linha LF, consistente com os CSVs já
        # versionados (o default do csv é "\r\n").
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _parse_args():
    import argparse
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--matrix", default=str(DEFAULT_MATRIX))
    p.add_argument("--generated-dir", default=str(DEFAULT_GENERATED))
    p.add_argument("--implementations-dir", default=str(DEFAULT_IMPL))
    p.add_argument("--out", default=str(REPO_ROOT / "evaluation" / "mutation_summary.csv"))
    p.add_argument("--survivors-out",
                   default=str(REPO_ROOT / "evaluation" / "mutation_survivors.csv"))
    p.add_argument("--strategy", choices=[*STRATEGIES, "all"], default="all")
    p.add_argument("--limit", type=int, default=0,
                   help="Limita o número de requisitos (0 = todos).")
    p.add_argument("--timeout", type=int, default=120,
                   help="Timeout (s) por execução do mutmut em uma config.")
    return p.parse_args()


def main():
    args = _parse_args()
    impl_root = Path(args.implementations_dir)
    generated_root = Path(args.generated_dir)
    strategies = list(STRATEGIES) if args.strategy == "all" else [args.strategy]

    req_dirs = sorted(d for d in impl_root.glob("req_*") if d.is_dir())
    if args.limit:
        req_dirs = req_dirs[:args.limit]
    if not req_dirs:
        sys.exit(f"Nenhuma implementação encontrada em {impl_root}")

    summary_all, survivors_all = [], []
    for req_dir in req_dirs:
        req_id = req_dir.name
        for strategy in strategies:
            if not (generated_root / strategy / f"test_{req_id}.py").exists():
                print(f"[skip] {strategy}/{req_id}: teste não gerado.")
                continue
            print(f"[run] {strategy}/{req_id} ...")
            summary, survivors = evaluate_config(
                req_id, strategy, timeout=args.timeout, matrix_path=Path(args.matrix),
                generated_dir=generated_root, impl_dir=impl_root,
            )
            summary_all.append(summary)
            survivors_all.extend(survivors)
            print(f"  -> status={summary['status']} "
                  f"score={summary['mutation_score_auto']} "
                  f"({summary['mutants_killed']}/{summary['mutants_total']} mortos)")

    if not summary_all:
        sys.exit("Nenhuma config avaliada. Gere os testes antes (generate_tests.py).")

    _write_csv(Path(args.out), SUMMARY_FIELDS, summary_all)
    _write_csv(Path(args.survivors_out), SURVIVOR_FIELDS, survivors_all)
    print(f"\nSummary -> {args.out}  ({len(summary_all)} configs)")
    print(f"Survivors -> {args.survivors_out}  ({len(survivors_all)} mutantes não-mortos)")


if __name__ == "__main__":
    main()
