#!/usr/bin/env python3
"""Calcula as métricas de avaliação a partir de ``results_matrix.csv``.

Métricas (definições da spec / CLAUDE.md):

    valid_rate        = testes executáveis / testes gerados
    correct_pass_rate = testes que passam na correta / testes executáveis
    bug_detection_rate= testes úteis / testes que passam na correta
    mutation_score    = mutantes mortos / total de mutantes (por requisito)

Também reporta redundância (testes que matam exatamente o mesmo conjunto de
bugs) e quebra tudo por estratégia (direct x two_step → RQ5).

Fase 4 (comparação controlando por volume): ``min_suite_size`` (suíte mínima por
set-cover guloso), ``essential_tests`` (kills únicos) e ``kills_per_test_mean``.

Saída: ``evaluation/metrics_summary.csv`` + relatório no terminal.

Uso:
    python evaluation/metrics.py
"""

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

try:  # garante acentos legíveis no console (Windows usa cp1252 por padrão)
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_matrix(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def bug_columns(rows):
    return [c for c in rows[0].keys() if c.startswith("bug_")] if rows else []


def bugs_present(req_rows, bug_cols):
    """Colunas de bug que existem para este requisito (célula não vazia)."""
    present = []
    for c in bug_cols:
        if any((r.get(c) or "") != "" for r in req_rows):
            present.append(c)
    return present


def compute_group(rows, bug_cols):
    """Calcula métricas para um conjunto de linhas (uma estratégia, um ou todos req)."""
    generated = len(rows)
    executable = [r for r in rows if r["classification"] != "not_executable"]
    passing_correct = [r for r in rows if r["correct"] == "pass"]
    useful = [r for r in rows if r["classification"] == "useful"]

    # mutation score: por requisito, um bug é morto se algum teste que passa na
    # correta NÃO passa nele (fail/error).
    bugs_total = 0
    bugs_killed = 0
    by_req = defaultdict(list)
    for r in rows:
        by_req[r["requirement"]].append(r)
    for req, req_rows in by_req.items():
        present = bugs_present(req_rows, bug_cols)
        bugs_total += len(present)
        valid_tests = [r for r in req_rows if r["correct"] == "pass"]
        for c in present:
            if any((r.get(c) or "pass") != "pass" for r in valid_tests):
                bugs_killed += 1

    # redundância: testes úteis que compartilham o mesmo conjunto de bugs mortos.
    redundant = 0
    sig_groups = defaultdict(list)
    for r in useful:
        killed = frozenset(
            c for c in bug_cols if (r.get(c) or "pass") not in ("pass", "")
        )
        sig_groups[(r["requirement"], killed)].append(r["test"])
    for _, members in sig_groups.items():
        if len(members) > 1:
            redundant += len(members)

    def rate(num, den):
        return round(num / den, 4) if den else 0.0

    return {
        "generated": generated,
        "executable": len(executable),
        "valid_rate": rate(len(executable), generated),
        "passing_correct": len(passing_correct),
        "correct_pass_rate": rate(len(passing_correct), len(executable)),
        "useful": len(useful),
        "bug_detection_rate": rate(len(useful), len(passing_correct)),
        "bugs_total": bugs_total,
        "bugs_killed": bugs_killed,
        "mutation_score": rate(bugs_killed, bugs_total),
        "redundant_tests": redundant,
    }


def killset_of_row(row, bug_cols):
    """Mutantes ``(requirement, bug_col)`` que esta linha mata.

    Vazio se a linha não passa na correta (``invalid``) ou não detecta defeito
    algum (``weak``). Célula de bug vazia (`""`) conta como 'não matado'.
    """
    if row.get("correct") != "pass":
        return frozenset()
    req = row["requirement"]
    return frozenset(
        (req, c) for c in bug_cols
        if (row.get(c) or "pass") not in ("pass", "")
    )


def suite_minimization(rows, bug_cols):
    """Métricas que controlam por volume de testes (Fase 4).

    - ``min_suite_size``: tamanho da menor suíte (set-cover **guloso e
      determinístico**) que mata todos os mutantes detectáveis pelo grupo;
    - ``essential_tests``: nº de testes que são o ÚNICO matador de algum mutante
      (não-removíveis da suíte);
    - ``kills_per_test_mean``: média de mutantes mortos por teste **útil**;
    - ``candidate_tests``: testes que passam na correta (pool elegível).

    Como mutantes de requisitos diferentes são disjuntos, calcular sobre o grupo
    todo (uma estratégia) equivale a somar as suítes mínimas por requisito.
    """
    contributions = []          # (id_teste, killset) de testes que matam ≥1 mutante
    universe = set()
    killers = defaultdict(set)  # mutante -> {id_teste}
    candidate_tests = 0
    for r in rows:
        if r.get("correct") == "pass":
            candidate_tests += 1
        ks = killset_of_row(r, bug_cols)
        if not ks:
            continue
        tid = (r["requirement"], r["test"])
        contributions.append((tid, ks))
        universe |= ks
        for mutant in ks:
            killers[mutant].add(tid)

    useful = len(contributions)
    total_kills = sum(len(ks) for _, ks in contributions)
    kills_per_test_mean = round(total_kills / useful, 4) if useful else 0.0
    essential = {next(iter(ts)) for ts in killers.values() if len(ts) == 1}

    # set-cover guloso determinístico: ordena por id; a cada passo pega o maior
    # ganho (empate -> primeiro na ordem ordenada, via comparação estrita).
    pool = sorted(contributions, key=lambda tc: tc[0])
    covered = set()
    min_suite_size = 0
    while covered != universe:
        best = None
        best_gain = 0
        for tid, ks in pool:
            gain = len(ks - covered)
            if gain > best_gain:
                best_gain = gain
                best = (tid, ks)
        if best is None:
            break
        covered |= best[1]
        pool.remove(best)
        min_suite_size += 1

    return {
        "min_suite_size": min_suite_size,
        "essential_tests": len(essential),
        "kills_per_test_mean": kills_per_test_mean,
        "candidate_tests": candidate_tests,
    }


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--matrix", default=str(REPO_ROOT / "evaluation" / "results_matrix.csv"))
    p.add_argument("--out", default=str(REPO_ROOT / "evaluation" / "metrics_summary.csv"))
    return p.parse_args()


def main():
    args = parse_args()
    matrix_path = Path(args.matrix)
    if not matrix_path.exists():
        raise SystemExit(f"Matriz não encontrada: {matrix_path}. Rode run_tests.py antes.")

    rows = load_matrix(matrix_path)
    if not rows:
        raise SystemExit("Matriz vazia.")
    bug_cols = bug_columns(rows)

    strategies = sorted({r["strategy"] for r in rows})
    requirements = sorted({r["requirement"] for r in rows})

    def metrics_for(group):
        # métricas brutas + métricas controlando por volume (Fase 4);
        # candidate_tests é redundante com passing_correct, fica fora do CSV.
        out = {**compute_group(group, bug_cols), **suite_minimization(group, bug_cols)}
        out.pop("candidate_tests", None)
        return out

    summary_rows = []
    for strat in strategies:
        strat_rows = [r for r in rows if r["strategy"] == strat]
        # agregado da estratégia
        summary_rows.append({"strategy": strat, "requirement": "ALL",
                             **metrics_for(strat_rows)})
        # por requisito
        for req in requirements:
            req_rows = [r for r in strat_rows if r["requirement"] == req]
            if req_rows:
                summary_rows.append({"strategy": strat, "requirement": req,
                                     **metrics_for(req_rows)})

    fieldnames = ["strategy", "requirement", "generated", "executable", "valid_rate",
                  "passing_correct", "correct_pass_rate", "useful", "bug_detection_rate",
                  "bugs_total", "bugs_killed", "mutation_score", "redundant_tests",
                  "min_suite_size", "essential_tests", "kills_per_test_mean"]
    out_path = Path(args.out)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary_rows)

    # relatório no terminal: comparação entre estratégias (linha ALL)
    print("\n" + "=" * 78)
    print("RESUMO DE MÉTRICAS  (linha ALL = agregado da estratégia)")
    print("=" * 78)
    header = (f"{'strategy':<10}{'req':<9}{'valid':>7}{'pass_ok':>9}"
              f"{'bug_det':>9}{'mut_sc':>8}{'useful':>8}{'redund':>8}")
    print(header)
    print("-" * 78)
    for row in summary_rows:
        print(f"{row['strategy']:<10}{row['requirement']:<9}"
              f"{row['valid_rate']:>7}{row['correct_pass_rate']:>9}"
              f"{row['bug_detection_rate']:>9}{row['mutation_score']:>8}"
              f"{row['useful']:>8}{row['redundant_tests']:>8}")
    print("=" * 78)

    # bloco Fase 4: comparação entre estratégias controlando por volume (ALL)
    print("\n" + "=" * 78)
    print("COMPARAÇÃO CONTROLANDO POR VOLUME  (Fase 4, linha ALL)")
    print("=" * 78)
    print(f"{'strategy':<10}{'useful':>8}{'bugs_killed':>12}{'min_suite':>11}"
          f"{'essential':>11}{'kills/test':>12}")
    print("-" * 78)
    for row in summary_rows:
        if row["requirement"] != "ALL":
            continue
        print(f"{row['strategy']:<10}{row['useful']:>8}{row['bugs_killed']:>12}"
              f"{row['min_suite_size']:>11}{row['essential_tests']:>11}"
              f"{row['kills_per_test_mean']:>12}")
    print("=" * 78)
    print(f"\nSalvo -> {out_path}")


if __name__ == "__main__":
    main()
