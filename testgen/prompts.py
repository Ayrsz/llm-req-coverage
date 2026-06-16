"""Construção dos prompts (funções puras, sem efeitos colaterais)."""

from __future__ import annotations

# Etapa 1 da Estratégia B: identificação de técnicas de teste.
TECHNIQUE_IDENTIFIER_PROMPT = "\n".join(
    [
        "You are a Software Testing Expert specialized in test technique selection.",
        "Given a test overview description, identify the most applicable functional test techniques.",
        "",
        "Available techniques:",
        "- equivalence partitioning",
        "- boundary value analysis",
        "- positive flow test",
        "- negative flow test",
        "- mandatory fields test",
        "- business rules test",
        "- state transition test",
        "- edge case test",
        "",
        "Return ONLY a comma-separated list of the most applicable techniques. "
        "No explanations, no extra text.",
    ]
)


def build_system_prompt_direct(requirement: str, example_overview: str, example_description: str) -> str:
    """System instruction da Estratégia A (geração direta)."""
    return "\n".join(
        [
            "You are a Senior Software Testing Engineer.",
            "Your objective is to generate technical, step-by-step test cases for specific functionalities.",
            "You must base your output STRICTLY on the provided requirements document.",
            "",
            "OUTPUT FORMAT:",
            "Every generated test case must STRICTLY follow this four-section structure.",
            "Do not add introductory or concluding remarks outside of this structure.",
            "",
            "1. Purpose",
            "2. Initial Conditions",
            "3. Steps/Description",
            "4. Expected Results",
            "",
            "=== REQUIREMENTS DOCUMENT (KNOWLEDGE BASE) ===",
            requirement,
            "==============================================",
            "",
            "EXPECTED TEST EXAMPLE:",
            "",
            f"DESCRIPTION: {example_overview}",
            "",
            "EXPECTED OUTPUT:",
            "",
            example_description,
        ]
    )


def build_system_prompt_two_step(requirement: str, example_overview: str, example_description: str) -> str:
    """System instruction da Estratégia B (geração guiada por técnicas)."""
    return "\n".join(
        [
            "You are a Senior Software Testing Engineer.",
            "Your objective is to generate technical, step-by-step test cases for specific functionalities.",
            "You must base your output STRICTLY on the provided requirements document.",
            "You will be given the test overview AND the applicable test techniques to guide the generation.",
            "",
            "OUTPUT FORMAT:",
            "Every generated test case must STRICTLY follow this structure.",
            "Do not add introductory or concluding remarks outside of this structure.",
            "",
            "Technique: [test technique(s) applied]",
            "Type: [Positive / Negative / Edge Case]",
            "",
            "1. Purpose",
            "2. Initial Conditions",
            "3. Steps/Description",
            "4. Expected Results",
            "",
            "=== REQUIREMENTS DOCUMENT (KNOWLEDGE BASE) ===",
            requirement,
            "==============================================",
            "",
            "EXPECTED TEST EXAMPLE:",
            "",
            f"DESCRIPTION: {example_overview}",
            "APPLICABLE TECHNIQUES: positive flow test",
            "",
            "EXPECTED OUTPUT:",
            "",
            "Technique: positive flow test",
            "Type: Positive",
            "",
            example_description,
        ]
    )


def build_user_prompt_direct(test_overview: str) -> str:
    return (
        "Considering all the specifications before, generate the test for the "
        "following overview. STRICTLY ONLY THE ANSWER.\n"
        f"TEST OVERVIEW: {test_overview}"
    )


def build_user_prompt_two_step(test_overview: str, techniques: str) -> str:
    return (
        "Considering all the specifications before, generate the test for the "
        "following overview using the identified techniques. STRICTLY ONLY THE ANSWER.\n"
        f"TEST OVERVIEW: {test_overview}\n"
        f"APPLICABLE TECHNIQUES: {techniques}"
    )


def build_technique_query(test_overview: str) -> str:
    return f"TEST OVERVIEW: {test_overview}"
