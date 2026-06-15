import pytest
from solution import age_bracket

@pytest.mark.parametrize(
    "age, expected_bracket",
    [
        # Casos inválidos (age < 0)
        (-1, "invalido"),  # AC1, Valor-limite inferior
        (-5, "invalido"),
        (-100, "invalido"),

        # Casos de criança (0 <= age <= 11)
        (0, "crianca"),    # AC2, Valor-limite inferior
        (1, "crianca"),
        (5, "crianca"),
        (11, "crianca"),   # AC2, Valor-limite superior

        # Casos de adolescente (12 <= age <= 17)
        (12, "adolescente"), # AC3, Valor-limite inferior
        (15, "adolescente"),
        (17, "adolescente"), # AC3, Valor-limite superior

        # Casos de adulto (18 <= age <= 59)
        (18, "adulto"),    # AC4, Valor-limite inferior
        (30, "adulto"),
        (45, "adulto"),
        (59, "adulto"),    # AC4, Valor-limite superior

        # Casos de idoso (age >= 60)
        (60, "idoso"),     # AC5, Valor-limite inferior
        (70, "idoso"),
        (100, "idoso"),
        (120, "idoso"),    # Valor-limite superior (exemplo de idade avançada)
    ]
)
def test_age_bracket_classification(age: int, expected_bracket: str):
    """
    Verifica a classificação da faixa etária para diferentes idades,
    incluindo casos típicos, de borda e inválidos.
    """
    assert age_bracket(age) == expected_bracket
