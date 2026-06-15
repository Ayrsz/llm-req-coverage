#!/usr/bin/env python3
"""Calcula as métricas de avaliação a partir de ``results_matrix.csv``.

Métricas (definições da spec / CLAUDE.md):

    valid_rate        = testes executáveis / testes gerados
    correct_pass_rate = testes que passam na correta / testes executáveis
    bug_detection_rate= testes úteis / testes que passam na correta
    mutation_score    = mutantes mortos / total de mutantes (por requisito)

Também reporta redundância (testes que matam exatamente o mesmo conjunto de
bugs) e quebra tudo por estratégia (direct x two_step → RQ5).

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

    summary_rows = []
    for strat in strategies:
        strat_rows = [r for r in rows if r["strategy"] == strat]
        # agregado da estratégia
        summary_rows.append({"strategy": strat, "requirement": "ALL",
                             **compute_group(strat_rows, bug_cols)})
        # por requisito
        for req in requirements:
            req_rows = [r for r in strat_rows if r["requirement"] == req]
            if req_rows:
                summary_rows.append({"strategy": strat, "requirement": req,
                                     **compute_group(req_rows, bug_cols)})

    fieldnames = ["strategy", "requirement", "generated", "executable", "valid_rate",
                  "passing_correct", "correct_pass_rate", "useful", "bug_detection_rate",
                  "bugs_total", "bugs_killed", "mutation_score", "redundant_tests"]
    out_path = Path(args.out)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
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
    print(f"\nSalvo -> {out_path}")


if __name__ == "__main__":
    main()
