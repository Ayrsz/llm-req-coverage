import pytest
from solution import bmi_category

# I. Cenários de Entradas Inválidas ("invalido")
@pytest.mark.parametrize(
    "weight, height, expected",
    [
        # 1. Altura exatamente zero (AC6)
        (70.0, 0.0, "invalido"),
        # 2. Altura negativa
        (70.0, -1.0, "invalido"),
        # 3. Peso negativo (AC7)
        (-1.0, 1.75, "invalido"),
        # 4. Ambos peso negativo e altura zero
        (-1.0, 0.0, "invalido"),
        # 5. Ambos peso negativo e altura negativa
        (-10.0, -1.0, "invalido"),
    ],
    ids=[
        "invalid_height_zero",
        "invalid_height_negative",
        "invalid_weight_negative",
        "invalid_weight_negative_height_zero",
        "invalid_weight_negative_height_negative",
    ],
)
def test_invalid_inputs(weight, height, expected):
    assert bmi_category(weight, height) == expected

# II. Cenários de Entradas Válidas - Classificação de IMC

# A. Categoria "abaixo" (IMC < 18.5)
@pytest.mark.parametrize(
    "weight, height, expected",
    [
        # 6. Peso zero, IMC = 0 (AC8)
        (0.0, 1.75, "abaixo"),
        # 7. Valor típico na faixa "abaixo" (AC1)
        (50.0, 1.75, "abaixo"),  # IMC ≈ 16.33
        # 8. IMC ligeiramente abaixo de 18.5
        (56.65624, 1.75, "abaixo"),  # IMC ≈ 18.49999
    ],
    ids=[
        "category_abaixo_weight_zero",
        "category_abaixo_typical",
        "category_abaixo_boundary_below_18_5",
    ],
)
def test_category_abaixo(weight, height, expected):
    assert bmi_category(weight, height) == expected

# B. Categoria "normal" (18.5 <= IMC < 25)
@pytest.mark.parametrize(
    "weight, height, expected",
    [
        # 9. IMC = 18.5, limite inferior inclusivo (AC2)
        (56.65625, 1.75, "normal"),  # IMC = 18.5
        # 10. Valor típico na faixa "normal" (AC3)
        (70.0, 1.75, "normal"),  # IMC ≈ 22.86
        # 11. IMC ligeiramente abaixo de 25
        (76.56249, 1.75, "normal"),  # IMC ≈ 24.99999
    ],
    ids=[
        "category_normal_boundary_at_18_5",
        "category_normal_typical",
        "category_normal_boundary_below_25",
    ],
)
def test_category_normal(weight, height, expected):
    assert bmi_category(weight, height) == expected

# C. Categoria "sobrepeso" (25 <= IMC < 30)
@pytest.mark.parametrize(
    "weight, height, expected",
    [
        # 12. IMC = 25.0, limite inferior inclusivo (AC4)
        (76.5625, 1.75, "sobrepeso"),  # IMC = 25.0
        # 13. Valor típico na faixa "sobrepeso"
        (85.0, 1.75, "sobrepeso"),  # IMC ≈ 27.76
        # 14. IMC ligeiramente abaixo de 30
        (91.87499, 1.75, "sobrepeso"),  # IMC ≈ 29.99999
    ],
    ids=[
        "category_sobrepeso_boundary_at_25",
        "category_sobrepeso_typical",
        "category_sobrepeso_boundary_below_30",
    ],
)
def test_category_sobrepeso(weight, height, expected):
    assert bmi_category(weight, height) == expected

# D. Categoria "obesidade" (IMC >= 30)
@pytest.mark.parametrize(
    "weight, height, expected",
    [
        # 15. IMC = 30.0, limite inferior inclusivo (AC5)
        (91.875, 1.75, "obesidade"),  # IMC = 30.0
        # 16. Valor típico na faixa "obesidade"
        (120.0, 1.75, "obesidade"),  # IMC ≈ 39.18
    ],
    ids=[
        "category_obesidade_boundary_at_30",
        "category_obesidade_typical",
    ],
)
def test_category_obesidade(weight, height, expected):
    assert bmi_category(weight, height) == expected

# III. Cenários de Borda e Tipos de Dados
@pytest.mark.parametrize(
    "weight, height, expected",
    [
        # 17. Entradas do tipo int, IMC = 17.5
        (70, 2, "abaixo"),
        # 18. Peso muito pequeno, mas válido, IMC muito pequeno
        (0.000000000000001, 1.0, "abaixo"),
        # 19. Altura muito pequena, mas válida, IMC muito grande
        (70.0, 0.000000000000001, "obesidade"),
        # 20. Peso extremamente alto, IMC = 1000
        (1000.0, 1.0, "obesidade"),
        # 21. Altura extremamente alta, IMC ≈ 11.11
        (100.0, 3.0, "abaixo"),
    ],
    ids=[
        "edge_case_int_inputs",
        "edge_case_very_small_positive_weight",
        "edge_case_very_small_positive_height",
        "edge_case_extremely_high_weight",
        "edge_case_extremely_high_height",
    ],
)
def test_edge_cases_and_data_types(weight, height, expected):
    assert bmi_category(weight, height) == expected
