"""Testes das estratégias de geração usando o FakeClient."""

import pytest

from testgen import config, prompts
from testgen.strategies import DirectStrategy, TwoStepStrategy, get_strategy

from .conftest import FakeClient


class TestDirectStrategy:
    def test_produces_text_and_no_techniques(self, sample_domain):
        client = FakeClient(default_text="DIRECT RESULT")
        strategy = DirectStrategy()
        sys = strategy.build_system_instruction(sample_domain)

        text, techniques = strategy.produce(client, sys, "Add a bookmark")

        assert text == "DIRECT RESULT"
        assert techniques == ""
        assert len(client.calls) == 1  # uma única chamada ao LLM


class TestTwoStepStrategy:
    def test_two_calls_technique_then_generation(self, sample_domain):
        # 1ª resposta = técnicas; 2ª resposta = teste gerado
        client = FakeClient(responses=["boundary value analysis", "TWO STEP RESULT"])
        strategy = TwoStepStrategy()
        sys = strategy.build_system_instruction(sample_domain)

        text, techniques = strategy.produce(client, sys, "Add a bookmark")

        assert techniques == "boundary value analysis"
        assert text == "TWO STEP RESULT"
        assert len(client.calls) == 2

    def test_technique_step_uses_low_temperature(self, sample_domain):
        client = FakeClient(responses=["positive flow test", "RESULT"])
        strategy = TwoStepStrategy()
        sys = strategy.build_system_instruction(sample_domain)

        strategy.produce(client, sys, "Add a bookmark")

        # 1ª chamada é a identificação de técnicas com temperatura baixa
        assert client.calls[0]["temperature"] == config.TECHNIQUE_TEMPERATURE
        assert client.calls[0]["system"] == prompts.TECHNIQUE_IDENTIFIER_PROMPT

    def test_techniques_injected_into_generation_prompt(self, sample_domain):
        client = FakeClient(responses=["equivalence partitioning", "RESULT"])
        strategy = TwoStepStrategy()
        sys = strategy.build_system_instruction(sample_domain)

        strategy.produce(client, sys, "Add a bookmark")

        # 2ª chamada (geração) deve conter as técnicas no prompt
        assert "equivalence partitioning" in client.calls[1]["prompt"]


class TestGetStrategy:
    def test_returns_correct_types(self):
        assert isinstance(get_strategy("A"), DirectStrategy)
        assert isinstance(get_strategy("b"), TwoStepStrategy)  # case-insensitive

    def test_unknown_raises(self):
        with pytest.raises(ValueError):
            get_strategy("Z")
