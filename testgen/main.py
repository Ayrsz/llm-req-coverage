"""Ponto de entrada (CLI) do experimento.

Exemplos:
    python -m testgen.main                          # todos os domínios, A e B
    python -m testgen.main --domains BOOKMARK       # só bookmark
    python -m testgen.main --strategies A           # só geração direta
"""

from __future__ import annotations

import argparse

try:  # carrega .env se python-dotenv estiver instalado
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from . import config, reporting
from .data_loader import load_domain_data
from .llm_client import GeminiClient
from .pipeline import ExperimentRunner
from .strategies import get_strategy


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera e avalia casos de teste a partir de requisitos via LLM.")
    parser.add_argument(
        "--domains",
        nargs="+",
        default=list(config.DOMAINS),
        choices=list(config.DOMAINS),
        help="Domínios a processar (padrão: todos).",
    )
    parser.add_argument(
        "--strategies",
        nargs="+",
        default=["A", "B"],
        choices=["A", "B"],
        help="Estratégias de geração (A=direta, B=duas etapas).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    client = GeminiClient()
    runner = ExperimentRunner(client)

    for domain_key in args.domains:
        spec = config.DOMAINS[domain_key]
        domain = load_domain_data(spec)

        results = []
        for code in args.strategies:
            strategy = get_strategy(code)
            print(f"\n>> Running {domain.name} | Strategy {code} ...")
            result = runner.run(domain, strategy)
            reporting.print_metrics(result)
            path = reporting.save_result(result)
            print(f"Saved: {path}")
            results.append(result)

        if len(results) > 1:
            reporting.print_comparison(domain.name, results)


if __name__ == "__main__":
    main()
