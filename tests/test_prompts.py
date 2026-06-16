"""Testes dos construtores de prompt (funções puras)."""

from testgen import prompts


class TestSystemPrompts:
    def test_direct_includes_requirement_and_example(self):
        out = prompts.build_system_prompt_direct("REQ DOC", "an overview", "a description")
        assert "REQ DOC" in out
        assert "an overview" in out
        assert "a description" in out
        assert "1. Purpose" in out

    def test_two_step_includes_technique_and_type_fields(self):
        out = prompts.build_system_prompt_two_step("REQ DOC", "an overview", "a description")
        assert "Technique:" in out
        assert "Type:" in out
        assert "REQ DOC" in out


class TestUserPrompts:
    def test_direct_contains_overview(self):
        out = prompts.build_user_prompt_direct("Add a bookmark")
        assert "Add a bookmark" in out

    def test_two_step_contains_overview_and_techniques(self):
        out = prompts.build_user_prompt_two_step("Add a bookmark", "boundary value analysis")
        assert "Add a bookmark" in out
        assert "boundary value analysis" in out


def test_technique_identifier_prompt_lists_techniques():
    assert "equivalence partitioning" in prompts.TECHNIQUE_IDENTIFIER_PROMPT
    assert "boundary value analysis" in prompts.TECHNIQUE_IDENTIFIER_PROMPT
