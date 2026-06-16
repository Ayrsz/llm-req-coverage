"""Saída: salvar CSVs e imprimir métricas/comparações."""

from __future__ import annotations

from pathlib import Path

from . import config
from .pipeline import ExperimentResult


def save_result(result: ExperimentResult, output_root: Path | None = None) -> Path:
    """Salva o CSV de um resultado em output/<subpasta>/<DOMINIO>_tests.csv."""
    from .strategies import get_strategy

    output_root = output_root or config.output_dir()
    subdir = get_strategy(result.strategy_code).output_subdir
    out_dir = output_root / subdir
    out_dir.mkdir(parents=True, exist_ok=True)

    path = out_dir / f"{result.domain}_tests.csv"
    result.records.to_csv(path, index=False, sep=";", encoding="utf-8-sig")
    return path


def print_metrics(result: ExperimentResult) -> None:
    m = result.metrics
    print(f"\n{'=' * 45}")
    print(f"METRICS — {result.domain} | Strategy {result.strategy_code}")
    print(f"{'=' * 45}")
    print(f"Total human tests  : {m.total_human}")
    print(f"Total generated    : {m.total_generated}")
    print(f"MATCH  (>=0.80)    : {m.matches}")
    print(f"REVIEW (0.65-0.79) : {m.reviews}")
    print(f"NO_MATCH (<0.65)   : {m.no_matches}")
    print(f"Precision          : {m.precision:.4f}")
    print(f"Recall             : {m.recall:.4f}")
    print(f"F1-Score           : {m.f1:.4f}")
    print(f"{'=' * 45}")


def print_comparison(domain: str, results: list[ExperimentResult]) -> None:
    """Tabela lado a lado das estratégias para um domínio."""
    print(f"\n{'=' * 70}")
    print(f"COMPARISON — {domain}")
    print(f"{'=' * 70}")
    header = f"{'Strategy':<12} {'MATCH':>7} {'REVIEW':>8} {'NO_MATCH':>10} {'Precision':>11} {'Recall':>9} {'F1':>8}"
    print(header)
    print("-" * 70)
    for result in results:
        m = result.metrics
        print(
            f"{result.strategy_code:<12} {m.matches:>7} {m.reviews:>8} {m.no_matches:>10} "
            f"{m.precision:>11.4f} {m.recall:>9.4f} {m.f1:>8.4f}"
        )
