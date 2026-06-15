import pytest
from solution import calculate_final_price

# 1. Testes de Classes de Equivalência (EP) e Casos Negativos/Invariantes para value negativo
@pytest.mark.parametrize(
    "value, customer_type, expected",
    [
        # Cenário: value negativo (preço final é 0.0)
        (-50.0, "common", 0.0),
        (-1.0, "premium", 0.0),
        # Cenário: value negativo (reforço)
        (-0.0001, "common", 0.0),
        # Cenário: Invariante: Preço final nunca negativo
        (-999.99, "premium", 0.0),
    ],
)
def test_negative_value_returns_zero(value, customer_type, expected):
    assert calculate_final_price(value, customer_type) == expected


# 2. Testes para 0 <= value <= 100 (sem desconto) e Valores-Limite
@pytest.mark.parametrize(
    "value, customer_type, expected",
    [
        # Cenário: 0 <= value <= 100 (sem desconto)
        (100.0, "common", 100.0),  # AC1
        (100.0, "premium", 100.0),
        (50.0, "common", 50.0),
        (50.0, "premium", 50.0),
        (0.0, "common", 0.0),
        # Cenário: Limite inferior para value > 0
        (0.01, "common", 0.01),
        # Cenário: Limite superior para value <= 100
        (99.99, "common", 99.99),
        # Cenário: Invariante: Preço final nunca maior que value (para value >= 0)
        (75.0, "common", 75.0),
    ],
)
def test_value_up_to_100_no_discount(value, customer_type, expected):
    assert calculate_final_price(value, customer_type) == pytest.approx(expected)


# 3. Testes para value > 100 e customer_type = "common" (5% de desconto)
@pytest.mark.parametrize(
    "value, customer_type, expected",
    [
        # Cenário: value > 100 e customer_type = "common" (5% de desconto)
        (200.0, "common", 190.0),  # AC2
        (150.0, "common", 142.50),
        # Cenário: Limite inferior para value > 100 (com desconto)
        (100.01, "common", 95.01),  # 100.01 * 0.95 = 95.0095 -> 95.01
        # Cenário: Valores extremos para value (muito grandes)
        (1_000_000.0, "common", 950_000.0),
    ],
)
def test_value_over_100_common_customer_5_percent_discount(value, customer_type, expected):
    assert calculate_final_price(value, customer_type) == pytest.approx(expected)


# 4. Testes para value > 100 e customer_type = "premium" (10% de desconto)
@pytest.mark.parametrize(
    "value, customer_type, expected",
    [
        # Cenário: value > 100 e customer_type = "premium" (10% de desconto)
        (200.0, "premium", 180.0),  # AC3
        (150.0, "premium", 135.00),
        # Cenário: Limite inferior para value > 100 (com desconto)
        (100.01, "premium", 90.01),  # 100.01 * 0.90 = 90.009 -> 90.01
        # Cenário: Valores extremos para value (muito grandes)
        (1_000_000.0, "premium", 900_000.0),
        # Cenário: Invariante: Preço final nunca maior que value (para value >= 0)
        (300.0, "premium", 270.0),
    ],
)
def test_value_over_100_premium_customer_10_percent_discount(value, customer_type, expected):
    assert calculate_final_price(value, customer_type) == pytest.approx(expected)


# 5. Testes para customer_type desconhecido (tratado como common)
@pytest.mark.parametrize(
    "value, customer_type, expected",
    [
        # Cenário: customer_type desconhecido (tratado como common)
        (200.0, "desconhecido", 190.0),  # AC5
        (200.0, "outro_tipo_qualquer", 190.0),
        # Cenário: customer_type com case sensitivity (não reconhecido)
        (200.0, "COMMON", 190.0),
        (200.0, "PREMIUM", 190.0),
        # Cenário: customer_type vazio ou com espaços em branco
        (200.0, "", 190.0),
        (200.0, "   ", 190.0),
    ],
)
def test_unknown_customer_type_treated_as_common(value, customer_type, expected):
    assert calculate_final_price(value, customer_type) == pytest.approx(expected)


# 6. Testes de arredondamento para 2 casas decimais
@pytest.mark.parametrize(
    "value, customer_type, expected",
    [
        # Cenário: Testes de arredondamento para 2 casas decimais (com round(x, 2))
        (105.263, "common", 100.00),  # 105.263 * 0.95 = 99.99985 -> 100.00
        (105.264, "common", 100.00),  # 105.264 * 0.95 = 100.0008 -> 100.00
        (105.265, "common", 100.00),  # 105.265 * 0.95 = 100.00175 -> 100.00
        (100.005, "common", 95.00),  # 100.005 * 0.95 = 95.00475 -> 95.00
        (100.015, "common", 95.01),  # 100.015 * 0.95 = 95.01425 -> 95.01
        (100.025, "common", 95.02),  # 100.025 * 0.95 = 95.02375 -> 95.02
    ],
)
def test_rounding_to_two_decimal_places(value, customer_type, expected):
    assert calculate_final_price(value, customer_type) == pytest.approx(expected)
