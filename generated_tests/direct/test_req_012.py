from solution import income_tax
import pytest


@pytest.mark.parametrize(
    "income, expected_tax",
    [
        (-100.0, 0.0),  # AC5: Rendimento negativo
        (-0.01, 0.0),
        (-1000.5, 0.0),
        (-0.000001, 0.0),
    ],
)
def test_negative_income_returns_zero(income: float, expected_tax: float):
    """
    Verifica que rendimentos negativos resultam em imposto zero.
    """
    assert income_tax(income) == pytest.approx(expected_tax)


@pytest.mark.parametrize(
    "income, expected_tax",
    [
        (0.0, 0.0),
        (1.0, 0.0),
        (1000.0, 0.0),
        (1999.99, 0.0),
        (2000.0, 0.0),  # AC1: Limite superior da faixa isenta (fechado)
    ],
)
def test_income_in_faixa1_is_exempt(income: float, expected_tax: float):
    """
    Verifica que rendimentos na primeira faixa (até 2000) são isentos.
    """
    assert income_tax(income) == pytest.approx(expected_tax)


@pytest.mark.parametrize(
    "income, expected_tax",
    [
        (2000.01, 0.00),  # (0.01 * 0.075) = 0.00075 -> 0.00
        (2000.07, 0.01),  # (0.07 * 0.075) = 0.00525 -> 0.01 (round half up)
        (2000.13, 0.01),  # (0.13 * 0.075) = 0.00975 -> 0.01 (round half up)
        (2000.14, 0.01),  # (0.14 * 0.075) = 0.0105 -> 0.01 (round half up)
        (2000.2, 0.02),  # (0.2 * 0.075) = 0.015 -> 0.02 (round half up)
        (2500.0, 37.50),  # AC6: Caso típico na Faixa 2 (500 * 0.075)
        (2999.99, 75.00),  # (999.99 * 0.075) = 74.99925 -> 75.00
        (3000.0, 75.00),  # AC2: Limite superior da Faixa 2 (1000 * 0.075)
    ],
)
def test_income_in_faixa2_only(income: float, expected_tax: float):
    """
    Verifica o cálculo do imposto para rendimentos que caem apenas na Faixa 2.
    Inclui casos de arredondamento 'round half up'.
    """
    assert income_tax(income) == pytest.approx(expected_tax)


@pytest.mark.parametrize(
    "income, expected_tax",
    [
        (3000.01, 75.00),  # 75.0 + (0.01 * 0.15) = 75.0015 -> 75.00
        (3000.03, 75.00),  # 75.0 + (0.03 * 0.15) = 75.0045 -> 75.00
        (3000.04, 75.01),  # 75.0 + (0.04 * 0.15) = 75.006 -> 75.01 (round half up)
        (3000.1, 75.02),  # 75.0 + (0.1 * 0.15) = 75.015 -> 75.02 (round half up)
        (3500.0, 150.00),  # 75.0 + (500 * 0.15) = 150.0
        (4499.99, 300.00),  # 75.0 + (1499.99 * 0.15) = 299.9985 -> 300.00
        (4500.0, 300.00),  # AC3: Limite superior da Faixa 3 (75.0 + 1500 * 0.15)
    ],
)
def test_income_in_faixa2_and_faixa3(income: float, expected_tax: float):
    """
    Verifica o cálculo do imposto para rendimentos que caem nas Faixas 2 e 3.
    Inclui casos de arredondamento 'round half up'.
    """
    assert income_tax(income) == pytest.approx(expected_tax)


@pytest.mark.parametrize(
    "income, expected_tax",
    [
        (4500.01, 300.00),  # 300.0 + (0.01 * 0.225) = 300.00225 -> 300.00
        (4500.02, 300.00),  # 300.0 + (0.02 * 0.225) = 300.0045 -> 300.00
        (4500.03, 300.01),  # 300.0 + (0.03 * 0.225) = 300.00675 -> 300.01 (round half up)
        (4500.04, 300.01),  # 300.0 + (0.04 * 0.225) = 300.009 -> 300.01
        (4500.07, 300.02),  # 300.0 + (0.07 * 0.225) = 300.01575 -> 300.02 (round half up)
        (5000.0, 412.50),  # AC4: Caso típico na Faixa 4 (300.0 + 500 * 0.225)
        (10000.0, 1537.50),  # Rendimento alto
        (100000.0, 21787.50),  # Rendimento muito alto
    ],
)
def test_income_in_faixa4_and_above(income: float, expected_tax: float):
    """
    Verifica o cálculo do imposto para rendimentos que caem nas Faixas 2, 3 e 4.
    Inclui casos de arredondamento 'round half up'.
    """
    assert income_tax(income) == pytest.approx(expected_tax)
