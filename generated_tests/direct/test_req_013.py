from solution import shipping_cost
import pytest


# Test cases for weight <= 0 (invalid input)
@pytest.mark.parametrize("weight, region, express, expected", [
    (0, "sul", False, 0.0),
    (0.0, "norte", True, 0.0),
    (-1, "sudeste", False, 0.0),  # AC6: shipping_cost(-1, "sul", True) == 0.0
    (-0.01, "centro-oeste", True, 0.0),
    (-100, "marte", False, 0.0),
])
def test_shipping_cost_invalid_weight_zero_or_less(weight, region, express, expected):
    assert shipping_cost(weight, region, express) == expected


# Test cases for base tariffs (weight <= 5, no express)
@pytest.mark.parametrize("weight, region, express, expected", [
    # AC1: shipping_cost(5, "sul", False) == 10.0
    (5, "sul", False, 10.0),
    (1, "sul", False, 10.0),
    (5, "sudeste", False, 10.0),
    (3.5, "sudeste", False, 10.0),

    # AC2: shipping_cost(5, "norte", False) == 20.0
    (5, "norte", False, 20.0),
    (1, "nordeste", False, 20.0),
    (5, "centro-oeste", False, 20.0),
    (2.5, "centro-oeste", False, 20.0),

    # AC5: shipping_cost(3, "marte", False) == 25.0
    (3, "marte", False, 25.0),
    (5, "desconhecida", False, 25.0),
    (1, "Sul", False, 25.0),  # Case-sensitive region
    (1, "", False, 25.0),  # Empty string region
])
def test_shipping_cost_base_tariffs_no_additional_no_express(weight, region, express, expected):
    assert shipping_cost(weight, region, express) == pytest.approx(expected)


# Test cases for additional weight cost (no express)
@pytest.mark.parametrize("weight, region, express, expected", [
    # AC3: shipping_cost(6, "sudeste", False) ≈ 12.0 (10 + 1*2)
    (6, "sudeste", False, 12.0),
    (5.01, "sul", False, 10.02),  # 10 + (0.01 * 2) = 10.02
    (7.5, "norte", False, 25.0),  # 20 + (2.5 * 2) = 25.0
    (10, "centro-oeste", False, 30.0),  # 20 + (5 * 2) = 30.0
    (10.25, "marte", False, 35.5),  # 25 + (5.25 * 2) = 25 + 10.5 = 35.5
])
def test_shipping_cost_additional_weight_no_express(weight, region, express, expected):
    assert shipping_cost(weight, region, express) == pytest.approx(expected)


# Test cases for express surcharge (no additional weight)
@pytest.mark.parametrize("weight, region, express, expected", [
    (5, "sul", True, 15.0),  # 10 * 1.5 = 15.0
    (5, "sudeste", True, 15.0),  # 10 * 1.5 = 15.0
    (5, "norte", True, 30.0),  # 20 * 1.5 = 30.0
    (5, "nordeste", True, 30.0),  # 20 * 1.5 = 30.0
    (5, "centro-oeste", True, 30.0),  # 20 * 1.5 = 30.0
    (5, "desconhecida", True, 37.5),  # 25 * 1.5 = 37.5
])
def test_shipping_cost_express_no_additional_weight(weight, region, express, expected):
    assert shipping_cost(weight, region, express) == pytest.approx(expected)


# Test cases for express surcharge with additional weight
@pytest.mark.parametrize("weight, region, express, expected", [
    # AC4: shipping_cost(6, "sul", True) ≈ 18.0 ((10 + 2) * 1.5)
    (6, "sul", True, 18.0),
    # AC7: shipping_cost(10, "nordeste", True) ≈ 45.0 ((20 + 5*2) * 1.5)
    (10, "nordeste", True, 45.0),
    (7.5, "sudeste", True, 22.5),  # (10 + 2.5*2) * 1.5 = (10 + 5) * 1.5 = 15 * 1.5 = 22.5
    (7.5, "norte", True, 37.5),  # (20 + 2.5*2) * 1.5 = (20 + 5) * 1.5 = 25 * 1.5 = 37.5
    (10.25, "marte", True, 53.25),  # (25 + 5.25*2) * 1.5 = (25 + 10.5) * 1.5 = 35.5 * 1.5 = 53.25
])
def test_shipping_cost_express_with_additional_weight(weight, region, express, expected):
    assert shipping_cost(weight, region, express) == pytest.approx(expected)


# Test cases specifically for rounding behavior (ROUND_HALF_UP)
@pytest.mark.parametrize("weight, region, express, expected", [
    # Cases where subtotal ends in .005, should round up
    (5.0025, "sul", False, 10.01),  # 10 + (0.0025 * 2) = 10.005 -> 10.01
    (5.0025, "norte", False, 20.01),  # 20 + (0.0025 * 2) = 20.005 -> 20.01
    (5.0025, "marte", False, 25.01),  # 25 + (0.0025 * 2) = 25.005 -> 25.01

    # Cases with express where final value ends in .005 or .0075, etc.
    # (10 + 0.0025*2) * 1.5 = 10.005 * 1.5 = 15.0075 -> 15.01
    (5.0025, "sul", True, 15.01),
    # (20 + 0.0025*2) * 1.5 = 20.005 * 1.5 = 30.0075 -> 30.01
    (5.0025, "norte", True, 30.01),
    # (25 + 0.0025*2) * 1.5 = 25.005 * 1.5 = 37.5075 -> 37.51

    # Cases where subtotal ends in .004, should round down
    (5.002, "sul", False, 10.00),  # 10 + (0.002 * 2) = 10.004 -> 10.00
    # (10 + 0.002*2) * 1.5 = 10.004 * 1.5 = 15.006 -> 15.01
    (5.002, "sul", True, 15.01),

    # Test a case where the rounding is exactly .5 (e.g., 15.75)
    # (10 + (5.25-5)*2) * 1.5 = (10 + 0.5) * 1.5 = 10.5 * 1.5 = 15.75
    (5.25, "sul", True, 15.75),
])
def test_shipping_cost_rounding_half_up(weight, region, express, expected):
    assert shipping_cost(weight, region, express) == pytest.approx(expected)


# Additional tests for edge cases not explicitly covered by ACs or previous parametrizations
@pytest.mark.parametrize("weight, region, express, expected", [
    # Large weight, all factors
    (100, "norte", True, 315.0),  # (20 + (95 * 2)) * 1.5 = (20 + 190) * 1.5 = 210 * 1.5 = 315.0
    # Large weight, no express
    (100, "sudeste", False, 200.0),  # 10 + (95 * 2) = 10 + 190 = 200.0

    # Very small positive weight (no additional, no express)
    (0.001, "sul", False, 10.0),
    # Very small positive weight (no additional, with express)
    (0.001, "sul", True, 15.0),

    # Weight exactly 5.0, different regions, express
    (5.0, "sul", True, 15.0),  # (10 + 0) * 1.5 = 15.0
    (5.0, "norte", True, 30.0),  # (20 + 0) * 1.5 = 30.0
    (5.0, "marte", True, 37.5),  # (25 + 0) * 1.5 = 37.5

    # Weight slightly less than 5.0
    (4.99, "sul", False, 10.0),
    (4.99, "norte", True, 30.0),  # 20 * 1.5 = 30.0

    # Weight slightly more than 5.0, with express, leading to specific rounding
    # (10 + (5.001-5)*2) * 1.5 = (10 + 0.002) * 1.5 = 10.002 * 1.5 = 15.003 -> 15.00
    (5.001, "sul", True, 15.00),
    # (10 + (5.003-5)*2) * 1.5 = (10 + 0.006) * 1.5 = 10.006 * 1.5 = 15.009 -> 15.01
    (5.003, "sul", True, 15.01),
])
def test_shipping_cost_various_edge_and_complex_cases(weight, region, express, expected):
    assert shipping_cost(weight, region, express) == pytest.approx(expected)
