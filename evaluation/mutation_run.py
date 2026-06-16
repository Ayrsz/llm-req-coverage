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

import re
from dataclasses import dataclass, field

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
