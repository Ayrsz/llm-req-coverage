#!/usr/bin/env python3
"""Executa cada teste gerado contra a implementação correta e as defeituosas.

Para cada (requisito x estratégia x arquivo de teste x variante de implementação):

1. cria um diretório temporário isolado;
2. copia a variante escolhida como ``solution.py`` (o teste importa ``solution``);
3. copia o arquivo de teste;
4. roda ``pytest --junitxml`` via subprocess com timeout;
5. lê o junitxml para obter o resultado por FUNÇÃO de teste.

Saída: ``evaluation/results_matrix.csv`` — uma linha por teste, com o resultado
em cada variante (pass/fail/error) e a classificação (useful/weak/invalid/
not_executable), conforme a tabela das seções 8/11 da spec.

Uso:
    python evaluation/run_tests.py
    python evaluation/run_tests.py --timeout 20
"""

import argparse
import csv
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

try:  # garante acentos legíveis no console (Windows usa cp1252 por padrão)
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parents[1]
STRATEGIES = ("direct", "two_step")


def discover_variants(impl_req_dir):
    """Retorna [(nome, caminho)] com 'correct' primeiro, depois bug_* ordenados."""
    correct = impl_req_dir / "correct.py"
    bugs = sorted(impl_req_dir.glob("bug_*.py"))
    variants = []
    if correct.exists():
        variants.append(("correct", correct))
    variants += [(b.stem, b) for b in bugs]
    return variants


def parse_junit(xml_path):
    """Lê o junitxml e devolve {nome_do_teste: status}.

    status ∈ {'pass', 'fail', 'error', 'skip'}. Devolve {} se não houver
    nenhum testcase (ex.: erro de coleta / sintaxe).
    """
    if not xml_path.exists():
        return {}
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError:
        return {}
    results = {}
    for tc in root.iter("testcase"):
        name = tc.get("name") or "<unnamed>"
        status = "pass"
        for child in tc:
            tag = child.tag.lower()
            if tag == "failure":
                status = "fail"
            elif tag == "error":
                status = "error"
            elif tag == "skipped":
                status = "skip"
        results[name] = status
    return results


def run_against_variant(test_file, variant_path, timeout):
    """Roda o arquivo de teste contra uma variante. Devolve {teste: status}."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copyfile(variant_path, tmp / "solution.py")
        shutil.copyfile(test_file, tmp / "test_generated.py")
        junit = tmp / "junit.xml"
        try:
            subprocess.run(
                [sys.executable, "-m", "pytest", "test_generated.py",
                 f"--junitxml={junit}", "-q", "-p", "no:cacheprovider"],
                cwd=tmp, timeout=timeout,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        except subprocess.TimeoutExpired:
            return {"<timeout>": "error"}
        return parse_junit(junit)


def classify(correct_status, bug_statuses):
    """Classifica um teste conforme a tabela da spec (seções 8/11)."""
    if correct_status == "error":
        return "not_executable"
    if correct_status != "pass":  # fail/skip na implementação correta
        return "invalid"
    # passou na correta -> detecta defeito se NÃO passa em alguma defeituosa
    if any(status != "pass" for status in bug_statuses.values()):
        return "useful"
    return "weak"


def evaluate_pair(req_id, strategy, test_file, variants, timeout):
    """Avalia um arquivo de teste contra todas as variantes do requisito.

    Devolve uma lista de linhas (dicts) — uma por função de teste.
    """
    # roda contra cada variante
    per_variant = {}  # nome_variante -> {teste: status}
    for vname, vpath in variants:
        per_variant[vname] = run_against_variant(test_file, vpath, timeout)

    correct_results = per_variant.get("correct", {})
    bug_names = [v for v, _ in variants if v != "correct"]

    # conjunto de testes vindos da execução na implementação correta
    test_names = sorted(correct_results)
    if not test_names:
        # nenhum teste coletou na correta -> arquivo não executável
        return [{
            "requirement": req_id, "strategy": strategy, "test": "<collection_error>",
            "correct": "error",
            **{b: "error" for b in bug_names},
            "classification": "not_executable",
        }]

    rows = []
    for tname in test_names:
        correct_status = correct_results.get(tname, "error")
        bug_statuses = {b: per_variant.get(b, {}).get(tname, "error") for b in bug_names}
        rows.append({
            "requirement": req_id, "strategy": strategy, "test": tname,
            "correct": correct_status,
            **bug_statuses,
            "classification": classify(correct_status, bug_statuses),
        })
    return rows


def parse_args():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--implementations-dir", default=str(REPO_ROOT / "implementations"))
    p.add_argument("--generated-dir", default=str(REPO_ROOT / "generated_tests"))
    p.add_argument("--out", default=str(REPO_ROOT / "evaluation" / "results_matrix.csv"))
    p.add_argument("--timeout", type=int, default=30,
                   help="Timeout (s) por execução de pytest, evita travamento.")
    return p.parse_args()


def main():
    args = parse_args()
    impl_root = Path(args.implementations_dir)
    gen_root = Path(args.generated_dir)

    req_dirs = sorted(d for d in impl_root.glob("req_*") if d.is_dir())
    if not req_dirs:
        sys.exit(f"Nenhuma implementação encontrada em {impl_root}")

    all_rows = []
    max_bugs = 0
    for req_dir in req_dirs:
        req_id = req_dir.name
        variants = discover_variants(req_dir)
        max_bugs = max(max_bugs, sum(1 for v, _ in variants if v != "correct"))
        for strategy in STRATEGIES:
            test_file = gen_root / strategy / f"test_{req_id}.py"
            if not test_file.exists():
                print(f"[skip] {strategy}/{req_id}: teste não gerado ainda.")
                continue
            print(f"[run] {strategy}/{req_id} contra {len(variants)} variantes ...")
            rows = evaluate_pair(req_id, strategy, test_file, variants, args.timeout)
            all_rows.extend(rows)

    if not all_rows:
        sys.exit("Nenhum teste para avaliar. Rode generate_tests.py primeiro.")

    bug_cols = [f"bug_{i:03d}" for i in range(1, max_bugs + 1)]
    fieldnames = ["requirement", "strategy", "test", "correct", *bug_cols, "classification"]

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval="")
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)

    print(f"\nMatriz salva -> {out_path}  ({len(all_rows)} linhas)")
    counts = {}
    for r in all_rows:
        counts[r["classification"]] = counts.get(r["classification"], 0) + 1
    print("Classificações:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
