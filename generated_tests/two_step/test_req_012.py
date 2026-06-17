import pytest
from solution import income_tax

# Testes para Classes de Equivalência, Entradas Inválidas e Valores-Limite gerais
@pytest.mark.parametrize(
    "income, expected_tax",
    [
        # EP1: Rendimento Negativo / Entradas Inválidas / Invariante
        (-100.0, 0.0),
        (-0.01, 0.0),
        (-1.0, 0.0),
        (-1000.0, 0.0),
        (-0.000001, 0.0),
        (-50.0, 0.0),

        # EP2: Faixa 1 (Isento) / BVA Limite 0 e 2000
        (0.0, 0.0),
        (0.01, 0.0),
        (1000.0, 0.0),
        (1999.99, 0.0),
        (2000.0, 0.0), # AC1

        # EP3: Faixa 2 (Parcial e Cheia) / BVA Limite 2000 e 3000
        (2000.01, 0.00), # (0.01 * 0.075 = 0.00075 -> 0.00)
        (2500.0, 37.5), # AC6 (500 * 0.075)
        (2999.99, 75.00), # (999.99 * 0.075 = 74.99925 -> 75.00 com ROUND_HALF_UP)
        (3000.0, 75.0), # AC2 (1000 * 0.075)

        # EP4: Faixa 3 (Parcial e Cheia) / BVA Limite 3000 e 4500
        (3000.01, 75.00), # (75.0 + 0.01 * 0.15 = 75.0015 -> 75.00)
        (3500.0, 150.0), # (75.0 + 500 * 0.15 = 75.0 + 75.0)
        (4499.99, 300.00), # (75.0 + 1499.99 * 0.15 = 75.0 + 224.9985 -> 300.00 com ROUND_HALF_UP)
        (4500.0, 300.0), # AC3 (75.0 + 1500 * 0.15)

        # EP5: Faixa 4 (Parcial e Maior Valor) / BVA Limite 4500 / Borda Grande Valor
        (4500.01, 300.00), # (300.0 + 0.01 * 0.225 = 300.00225 -> 300.00)
        (5000.0, 412.5), # AC4 (300.0 + 500 * 0.225 = 300.0 + 112.5)
        (10000.0, 1537.5), # (300.0 + 5500 * 0.225 = 300.0 + 1237.5)
        (1000000.0, 224287.5), # (300.0 + 995500 * 0.225)
    ]
)
def test_income_tax_general_scenarios(income: float, expected_tax: float):
    assert income_tax(income) == pytest.approx(expected_tax)

# Testes específicos para o comportamento de arredondamento (Round Half Up)
@pytest.mark.parametrize(
    "income, expected_tax",
    [
        # Arredondamento: X.XX5 -> X.X(X+1)
        (2000 + 1/15, 0.01), # (1/15) * 0.075 = 0.005 -> 0.01
        (3000 + 1/30, 75.01), # 75.0 + (1/30) * 0.15 = 75.0 + 0.005 = 75.005 -> 75.01
        (4500 + 1/45, 300.01), # 300.0 + (1/45) * 0.225 = 300.0 + 0.005 = 300.005 -> 300.01

        # Arredondamento: X.XX4 -> X.XX
        (2000 + 4/75, 0.00), # (4/75) * 0.075 = 0.004 -> 0.00
        (3000 + 2/75, 75.00), # 75.0 + (2/75) * 0.15 = 75.0 + 0.004 = 75.004 -> 75.00
        (4500 + 4/225, 300.00), # 300.0 + (4/225) * 0.225 = 300.0 + 0.004 = 300.004 -> 300.00
    ]
)
def test_income_tax_rounding_cases(income: float, expected_tax: float):
    assert income_tax(income) == pytest.approx(expected_tax)

# Testes para os Critérios de Aceitação (ACs)
# Estes testes são redundantes com os parametrizados acima, mas garantem cobertura explícita dos ACs.
def test_acceptance_criteria_ac1():
    # AC1. income_tax(2000) == 0.0 (limite fechado, isento).
    assert income_tax(2000) == pytest.approx(0.0)

def test_acceptance_criteria_ac2():
    # AC2. income_tax(3000) ≈ 75.0 (faixa 2 cheia: 1000 * 0.075).
    assert income_tax(3000) == pytest.approx(75.0)

def test_acceptance_criteria_ac3():
    # AC3. income_tax(4500) ≈ 300.0 (faixas 2 + 3: 75.0 + 225.0).
    assert income_tax(4500) == pytest.approx(300.0)

def test_acceptance_criteria_ac4():
    # AC4. income_tax(5000) ≈ 412.5 (75.0 + 225.0 + 500 * 0.225).
    assert income_tax(5000) == pytest.approx(412.5)

def test_acceptance_criteria_ac5():
    # AC5. income_tax(-100) == 0.0 (invariante, entrada inválida).
    assert income_tax(-100) == pytest.approx(0.0)

def test_acceptance_criteria_ac6():
    # AC6. income_tax(2500) ≈ 37.5 (só faixa 2: 500 * 0.075).
    assert income_tax(2500) == pytest.approx(37.5)
