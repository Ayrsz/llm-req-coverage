#!/usr/bin/env python3
"""Gera testes pytest a partir dos requisitos em linguagem natural usando o LLM.

Duas estratégias de prompting (RQ5):

- ``direct``: requisito -> 1 chamada -> testes pytest.
- ``two_step``: requisito -> identificação de técnicas/cenários -> testes pytest.

Saída: ``generated_tests/<estrategia>/test_<req>.py``.

Uso:
    python evaluation/generate_tests.py                 # todos os requisitos, ambas estratégias
    python evaluation/generate_tests.py --limit 1       # smoke test (1 requisito)
    python evaluation/generate_tests.py --strategy direct --sleep 7
"""

import argparse
import re
import sys
from pathlib import Path

import llm_client  # módulo irmão em evaluation/

try:  # garante acentos legíveis no console (Windows usa cp1252 por padrão)
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = REPO_ROOT / "prompts"

STRATEGIES = ("direct", "two_step")


def read_prompt(name):
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def strip_code_fences(text):
    """Extrai o código de uma resposta do LLM, removendo cercas markdown.

    Aceita blocos ```python ... ``` ou ``` ... ```. Se não houver cerca,
    devolve o texto como veio (apenas com espaços das pontas removidos).
    """
    fenced = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    if fenced:
        return fenced.group(1).strip() + "\n"
    return text.strip() + "\n"


def gen_direct(client, args, requirement):
    prompt = read_prompt("direct_prompt.txt").format(requirement=requirement)
    raw = llm_client.generate(
        client, args.model, prompt,
        temperature=args.temperature, cache_dir=args.cache_dir, sleep=args.sleep,
    )
    return strip_code_fences(raw)


def gen_two_step(client, args, requirement):
    step1 = read_prompt("technique_identification_prompt.txt").format(requirement=requirement)
    scenarios = llm_client.generate(
        client, args.model, step1,
        temperature=args.temperature, cache_dir=args.cache_dir, sleep=args.sleep,
    )
    step2 = read_prompt("pytest_generation_prompt.txt").format(
        requirement=requirement, scenarios=scenarios
    )
    raw = llm_client.generate(
        client, args.model, step2,
        temperature=args.temperature, cache_dir=args.cache_dir, sleep=args.sleep,
    )
    return strip_code_fences(raw)


GENERATORS = {"direct": gen_direct, "two_step": gen_two_step}


def parse_args():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--requirements-dir", default=str(REPO_ROOT / "requirements"))
    p.add_argument("--out-dir", default=str(REPO_ROOT / "generated_tests"))
    p.add_argument("--strategy", choices=[*STRATEGIES, "all"], default="all")
    p.add_argument("--model", default=llm_client.DEFAULT_MODEL)
    p.add_argument("--temperature", type=float, default=0.0,
                   help="Use 0 para geração determinística (recomendado para reprodutibilidade).")
    p.add_argument("--limit", type=int, default=0,
                   help="Limita o número de requisitos (0 = todos). Útil para smoke tests.")
    p.add_argument("--sleep", type=float, default=0.0,
                   help="Pausa em segundos entre chamadas (respeita limite por minuto do free tier).")
    p.add_argument("--cache-dir", default=str(REPO_ROOT / "evaluation" / ".cache"))
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--api-key", default=None)
    return p.parse_args()


def main():
    args = parse_args()
    args.cache_dir = None if args.no_cache else Path(args.cache_dir)
    client = llm_client.build_client(args.api_key)

    strategies = list(STRATEGIES) if args.strategy == "all" else [args.strategy]

    req_files = sorted(Path(args.requirements_dir).glob("req_*.md"))
    if not req_files:
        sys.exit(f"Nenhum requisito encontrado em {args.requirements_dir}")
    if args.limit:
        req_files = req_files[:args.limit]

    for req_path in req_files:
        req_id = req_path.stem  # ex.: req_001
        requirement = req_path.read_text(encoding="utf-8")
        for strategy in strategies:
            print(f"[{strategy}] {req_id} ...")
            code = GENERATORS[strategy](client, args, requirement)
            out_dir = Path(args.out_dir) / strategy
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"test_{req_id}.py"
            out_path.write_text(code, encoding="utf-8")
            print(f"  -> {out_path}")


if __name__ == "__main__":
    main()
