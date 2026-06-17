import pytest
from solution import calculate_final_price


@pytest.mark.parametrize(
    "value, customer_type, expected_price",
    [
        # Casos Negativos / Análise de Valores-Limite / Invariantes (AC4)
        (-50.0, "common", 0.0),
        (-0.01, "premium", 0.0),
        (-100.0, "common", 0.0),
    ],
    ids=[
        "negative_value_common",
        "negative_value_premium_close_to_zero",
        "negative_value_large",
    ],
)
def test_calculate_final_price_negative_values_return_zero(
    value, customer_type, expected_price
):
    """
    Testa que valores de entrada negativos resultam em preço final 0.0.
    Cobre AC4 e outros casos negativos.
    """
    assert calculate_final_price(value, customer_type) == pytest.approx(expected_price)


@pytest.mark.parametrize(
    "value, customer_type, expected_price",
    [
        # Análise de Valores-Limite / Classes de Equivalência (0 <= value <= 100)
        (0.0, "common", 0.0),
        (0.01, "premium", 0.01),
        (50.0, "common", 50.0),
        (50.0, "premium", 50.0),
        (99.99, "common", 99.99),
        (100.0, "common", 100.0),  # AC1
        (100.0, "premium", 100.0),
        # Casos de Borda / Arredondamento (sem desconto)
        (95.015, "common", 95.02),  # 95.015 arredondado para 95.02
    ],
    ids=[
        "value_zero",
        "value_just_above_zero_premium",
        "value_mid_range_common",
        "value_mid_range_premium",
        "value_just_below_limit",
        "value_at_limit_common_AC1",
        "value_at_limit_premium",
        "rounding_no_discount",
    ],
)
def test_calculate_final_price_no_discount_up_to_100(
    value, customer_type, expected_price
):
    """
    Testa que não há desconto para compras de valor <= 100.0,
    independentemente do tipo de cliente.
    Cobre AC1 e casos de arredondamento sem desconto.
    """
    assert calculate_final_price(value, customer_type) == pytest.approx(expected_price)


@pytest.mark.parametrize(
    "value, customer_type, expected_price",
    [
        # Análise de Valores-Limite / Classes de Equivalência (value > 100, common)
        (100.01, "common", 95.01),  # 100.01 * 0.95 = 95.0095 -> 95.01
        (200.0, "common", 190.0),  # AC2
        (1000.0, "common", 950.0),
        # Casos de Borda / Arredondamento (common)
        (142.975, "common", 135.83),  # 142.975 * 0.95 = 135.82625 -> 135.83
        (100.005, "common", 95.00),  # 100.005 * 0.95 = 95.00475 -> 95.00
        (100.015, "common", 95.01),  # 100.015 * 0.95 = 95.01425 -> 95.01
        (
            100.00000000000001,
            "common",
            95.00,
        ),  # 100.00000000000001 * 0.95 = 95.0000000000000095 -> 95.00
    ],
    ids=[
        "value_just_above_limit_common",
        "value_200_common_AC2",
        "value_1000_common",
        "rounding_common_half_up_1",
        "rounding_common_half_up_2",
        "rounding_common_half_up_3",
        "rounding_common_float_precision",
    ],
)
def test_calculate_final_price_discount_common_customer(
    value, customer_type, expected_price
):
    """
    Testa o cálculo de desconto de 5% para clientes 'common' em compras > 100.0.
    Cobre AC2 e casos de arredondamento.
    """
    assert calculate_final_price(value, customer_type) == pytest.approx(expected_price)


@pytest.mark.parametrize(
    "value, customer_type, expected_price",
    [
        # Análise de Valores-Limite / Classes de Equivalência (value > 100, premium)
        (100.01, "premium", 90.01),  # 100.01 * 0.90 = 90.009 -> 90.01
        (200.0, "premium", 180.0),  # AC3
        (1000.0, "premium", 900.0),
        # Casos de Borda / Arredondamento (premium)
        (142.975, "premium", 128.68),  # 142.975 * 0.90 = 128.6775 -> 128.68
        (100.005, "premium", 90.00),  # 100.005 * 0.90 = 90.0045 -> 90.00
        (100.015, "premium", 90.01),  # 100.015 * 0.90 = 90.0135 -> 90.01
    ],
    ids=[
        "value_just_above_limit_premium",
        "value_200_premium_AC3",
        "value_1000_premium",
        "rounding_premium_half_up_1",
        "rounding_premium_half_up_2",
        "rounding_premium_half_up_3",
    ],
)
def test_calculate_final_price_discount_premium_customer(
    value, customer_type, expected_price
):
    """
    Testa o cálculo de desconto de 10% para clientes 'premium' em compras > 100.0.
    Cobre AC3 e casos de arredondamento.
    """
    assert calculate_final_price(value, customer_type) == pytest.approx(expected_price)


@pytest.mark.parametrize(
    "value, customer_type, expected_price",
    [
        # Classes de Equivalência / Casos Negativos (customer_type desconhecido)
        (200.0, "desconhecido", 190.0),  # AC5
        (200.0, "", 190.0),
        (200.0, "COMMON", 190.0),  # Case-insensitive, tratado como common
        (200.0, "PREMIUM", 180.0),  # Case-insensitive, tratado como premium
        (200.0, None, 190.0),  # None type, tratado como common
    ],
    ids=[
        "unknown_customer_type_AC5",
        "empty_customer_type",
        "uppercase_common_customer_type",
        "uppercase_premium_customer_type",
        "none_customer_type",
    ],
)
def test_calculate_final_price_unknown_customer_type_treated_as_common(
    value, customer_type, expected_price
):
    """
    Testa que tipos de cliente desconhecidos são tratados como 'common'.
    Cobre AC5 e variações de entrada para customer_type.
    """
    assert calculate_final_price(value, customer_type) == pytest.approx(expected_price)
