"""Estratégias de geração de teste (A: direta, B: duas etapas).

Cada estratégia sabe (1) montar sua system instruction a partir do domínio e
(2) produzir um teste para um dado overview, usando o ``LLMClient`` injetado.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from . import config, prompts
from .data_loader import DomainData
from .llm_client import LLMClient


class GenerationStrategy(ABC):
    """Interface comum às estratégias de geração."""

    #: identificador curto usado em relatórios/CSV (ex.: "A")
    code: str
    #: subpasta de saída (ex.: "direct_prompt")
    output_subdir: str

    @abstractmethod
    def build_system_instruction(self, domain: DomainData) -> str:
        ...

    @abstractmethod
    def produce(self, client: LLMClient, system_instruction: str, test_overview: str) -> tuple[str, str]:
        """Retorna (texto_do_teste, técnicas_identificadas).

        ``técnicas_identificadas`` é "" para estratégias que não as usam.
        """


class DirectStrategy(GenerationStrategy):
    """Estratégia A — o LLM gera o teste diretamente a partir do overview."""

    code = "A"
    output_subdir = "direct_prompt"

    def build_system_instruction(self, domain: DomainData) -> str:
        return prompts.build_system_prompt_direct(
            domain.requirement, domain.example_overview, domain.example_description
        )

    def produce(self, client: LLMClient, system_instruction: str, test_overview: str) -> tuple[str, str]:
        prompt = prompts.build_user_prompt_direct(test_overview)
        return client.generate(system_instruction, prompt), ""


class TwoStepStrategy(GenerationStrategy):
    """Estratégia B — identifica técnicas e depois gera o teste guiado por elas."""

    code = "B"
    output_subdir = "two_step_prompt"

    def build_system_instruction(self, domain: DomainData) -> str:
        return prompts.build_system_prompt_two_step(
            domain.requirement, domain.example_overview, domain.example_description
        )

    def produce(self, client: LLMClient, system_instruction: str, test_overview: str) -> tuple[str, str]:
        # Etapa 1: identificar técnicas aplicáveis (modelo agnóstico, temp baixa)
        techniques = client.generate(
            prompts.TECHNIQUE_IDENTIFIER_PROMPT,
            prompts.build_technique_query(test_overview),
            temperature=config.TECHNIQUE_TEMPERATURE,
        ).strip()

        # Etapa 2: gerar o teste guiado pelas técnicas
        prompt = prompts.build_user_prompt_two_step(test_overview, techniques)
        return client.generate(system_instruction, prompt), techniques


STRATEGIES: dict[str, type[GenerationStrategy]] = {
    "A": DirectStrategy,
    "B": TwoStepStrategy,
}


def get_strategy(code: str) -> GenerationStrategy:
    code = code.upper()
    if code not in STRATEGIES:
        raise ValueError(f"Estratégia desconhecida: {code!r}. Use uma de {list(STRATEGIES)}.")
    return STRATEGIES[code]()
