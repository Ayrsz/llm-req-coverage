import pytest
from solution import bmi_category

@pytest.mark.parametrize(
    "weight, height, expected",
    [
        # Casos inválidos (height <= 0 ou weight < 0)
        (70, 0, "invalido"),  # AC6: Altura zero
        (70, -1.75, "invalido"),  # Altura negativa
        (70, -0.0001, "invalido"),  # Altura negativa muito pequena
        (-1, 1.75, "invalido"),  # AC7: Peso negativo
        (-0.0001, 1.75, "invalido"),  # Peso negativo muito pequeno
        (-1, 0, "invalido"),  # Ambos inválidos
        (-10, -10, "invalido"),  # Ambos inválidos
    ],
)
def test_bmi_category_invalid_inputs(weight, height, expected):
    """Testa casos de entrada inválida que devem retornar 'invalido'."""
    assert bmi_category(weight, height) == expected


@pytest.mark.parametrize(
    "weight, height, expected",
    [
        # AC8: Peso zero (válido, resulta em "abaixo")
        (0, 1.75, "abaixo"),
        (0.0, 1.75, "abaixo"),

        # Categoria "abaixo" (IMC < 18.5)
        (50, 1.75, "abaixo"),  # AC1: IMC ≈ 16.33 (típico)
        (56.65, 1.75, "abaixo"),  # IMC ≈ 18.496 (pouco abaixo de 18.5)
        (0.0001, 1.75, "abaixo"),  # Peso muito pequeno, IMC muito baixo
        (70, 2.0, "abaixo"), # IMC = 70 / (2*2) = 17.5

        # Categoria "normal" (18.5 <= IMC < 25)
        (56.66, 1.75, "normal"),  # AC2: IMC ≈ 18.5 (limite inferior incluso)
        (56.65625, 1.75, "normal"), # IMC = 18.5 (exato)
        (70, 1.75, "normal"),  # AC3: IMC ≈ 22.86 (típico)
        (76.5624, 1.75, "normal"),  # IMC ≈ 24.999 (pouco abaixo de 25)

        # Categoria "sobrepeso" (25 <= IMC < 30)
        (76.5625, 1.75, "sobrepeso"),  # AC4: IMC = 25.0 (limite inferior incluso)
        (80, 1.75, "sobrepeso"),  # IMC ≈ 26.12 (típico)
        (91.8749, 1.75, "sobrepeso"),  # IMC ≈ 29.999 (pouco abaixo de 30)

        # Categoria "obesidade" (IMC >= 30)
        (91.875, 1.75, "obesidade"),  # AC5: IMC = 30.0 (limite inferior incluso)
        (100, 1.75, "obesidade"),  # IMC ≈ 32.66 (típico)
        (200, 1.75, "obesidade"),  # Peso muito alto, IMC muito alto
        (70, 0.5, "obesidade"),  # Altura muito baixa, IMC muito alto (70 / 0.25 = 280)

        # Testes com tipos mistos (int/float)
        (50, 1, "obesidade"),  # IMC = 50 / 1 = 50
        (50.0, 1, "obesidade"),
        (50, 1.0, "obesidade"),
        (50.0, 1.0, "obesidade"),
    ],
)
def test_bmi_category_valid_inputs_and_categories(weight, height, expected):
    """Testa casos de entrada válida para todas as categorias de IMC."""
    assert bmi_category(weight, height) == expected


# Testes de borda explícitos para garantir a precisão dos limites
def test_bmi_category_boundary_18_5_exact():
    """Testa o limite exato de 18.5 (deve ser 'normal')."""
    # weight = 18.5 * (1.75 * 1.75) = 56.65625
    assert bmi_category(56.65625, 1.75) == "normal"


def test_bmi_category_boundary_18_5_just_below():
    """Testa um valor ligeiramente abaixo de 18.5 (deve ser 'abaixo')."""
    assert bmi_category(56.65624, 1.75) == "abaixo"


def test_bmi_category_boundary_25_exact():
    """Testa o limite exato de 25.0 (deve ser 'sobrepeso')."""
    # weight = 25.0 * (1.75 * 1.75) = 76.5625
    assert bmi_category(76.5625, 1.75) == "sobrepeso"


def test_bmi_category_boundary_25_just_below():
    """Testa um valor ligeiramente abaixo de 25.0 (deve ser 'normal')."""
    assert bmi_category(76.5624, 1.75) == "normal"


def test_bmi_category_boundary_30_exact():
    """Testa o limite exato de 30.0 (deve ser 'obesidade')."""
    # weight = 30.0 * (1.75 * 1.75) = 91.875
    assert bmi_category(91.875, 1.75) == "obesidade"


def test_bmi_category_boundary_30_just_below():
    """Testa um valor ligeiramente abaixo de 30.0 (deve ser 'sobrepeso')."""
    assert bmi_category(91.8749, 1.75) == "sobrepeso"


def test_bmi_category_extreme_height_low_bmi():
    """Testa com altura muito grande, resultando em IMC muito baixo."""
    assert bmi_category(70, 10.0) == "abaixo"  # IMC = 70 / 100 = 0.7


def test_bmi_category_extreme_weight_high_bmi():
    """Testa com peso muito grande, resultando em IMC muito alto."""
    assert bmi_category(1000, 1.75) == "obesidade"  # IMC ≈ 326.5
