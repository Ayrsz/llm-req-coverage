"""Fixtures compartilhadas — incluindo um cliente LLM fake (sem API)."""

from __future__ import annotations

import pandas as pd
import pytest

from testgen.data_loader import DomainData


class FakeClient:
    """Cliente LLM determinístico para testes — não chama nenhuma API.

    - ``generate`` devolve respostas de uma fila (ou um texto padrão) e registra
      todas as chamadas em ``self.calls`` para inspeção.
    - ``embed`` mapeia textos para vetores fixos via ``embeddings`` (texto ->
      vetor). Textos desconhecidos viram um vetor padrão, garantindo
      determinismo do score de similaridade.
    """

    def __init__(self, responses=None, embeddings=None, default_text="GENERATED TEST", default_embedding=None):
        self._responses = list(responses or [])
        self._embeddings = embeddings or {}
        self.default_text = default_text
        self.default_embedding = default_embedding or [1.0, 0.0, 0.0]
        self.calls: list[dict] = []

    def generate(self, system_instruction: str, prompt: str, temperature=None) -> str:
        self.calls.append(
            {"system": system_instruction, "prompt": prompt, "temperature": temperature}
        )
        if self._responses:
            return self._responses.pop(0)
        return self.default_text

    def embed(self, text: str):
        return self._embeddings.get(text, self.default_embedding)


@pytest.fixture
def fake_client():
    return FakeClient


@pytest.fixture
def sample_domain():
    """DomainData minimalista com dois casos a avaliar."""
    tests = pd.DataFrame(
        [
            {"ID": 1, "test-overview": "Add a bookmark", "test-description": "GT one"},
            {"ID": 2, "test-overview": "Remove a bookmark", "test-description": "GT two"},
        ]
    )
    return DomainData(
        name="BOOKMARK",
        requirement="REQUIREMENT DOC TEXT",
        example_overview="View bookmarks",
        example_description="EXAMPLE DESCRIPTION",
        tests=tests,
    )
