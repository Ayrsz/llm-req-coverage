import pytest
from solution import calculate_final_price

# Test cases for negative value (Rule 1: price final is 0.0)
@pytest.mark.parametrize("value, customer_type, expected_price", [
    (-50.0, "common", 0.0),  # AC4: Example from requirement
    (-0.01, "premium", 0.0), # Edge case: just below zero
    (-1000.0, "unknown", 0.0), # Large negative value with unknown customer type
    (-1.0, "common", 0.0),
])
def test_negative_value_returns_zero(value, customer_type, expected_price):
    assert calculate_final_price(value, customer_type) == pytest.approx(expected_price)

# Test cases for value <= 100 (Rule 2: no discount)
@pytest.mark.parametrize("value, customer_type, expected_price", [
    (0.0, "common", 0.0), # Edge case: zero value
    (50.0, "common", 50.0), # Typical case below 100
    (100.0, "common", 100.0),  # AC1: Boundary value, no discount
    (100.0, "premium", 100.0), # Boundary with premium customer
    (100.0, "desconhecido", 100.0), # Boundary with unknown customer
    (99.99, "common", 99.99), # Just below 100
    (0.01, "premium", 0.01), # Just above zero
])
def test_value_up_to_100_has_no_discount(value, customer_type, expected_price):
    assert calculate_final_price(value, customer_type) == pytest.approx(expected_price)

# Test cases for value > 100 with "common" or unknown customer type (Rule 3: 5% discount)
@pytest.mark.parametrize("value, customer_type, expected_price", [
    (200.0, "common", 190.0),  # AC2: Example from requirement
    (200.0, "desconhecido", 190.0), # AC5: Unknown type treated as common
    (200.0, "gold", 190.0), # Another unknown type
    (200.0, "", 190.0), # Empty string customer type
    (100.01, "common", 95.01), # Boundary: just above 100, 100.01 * 0.95 = 95.0095 -> 95.01
    (100.01, "unknown", 95.01), # Boundary with unknown type
    (150.50, "common", 142.98), # Typical float value, 150.50 * 0.95 = 142.975 -> 142.98
    (111.11, "common", 105.55), # Rounding check: 111.11 * 0.95 = 105.5545 -> 105.55
    (1000.0, "common", 950.0), # Large value
])
def test_value_over_100_common_or_unknown_customer_gets_5_percent_discount(value, customer_type, expected_price):
    assert calculate_final_price(value, customer_type) == pytest.approx(expected_price)

# Test cases for value > 100 with "premium" customer type (Rule 3: 10% discount)
@pytest.mark.parametrize("value, customer_type, expected_price", [
    (200.0, "premium", 180.0),  # AC3: Example from requirement
    (100.01, "premium", 90.01), # Boundary: just above 100, 100.01 * 0.90 = 90.009 -> 90.01
    (150.50, "premium", 135.45), # Typical float value, 150.50 * 0.90 = 135.45
    (111.11, "premium", 100.00), # Rounding check: 111.11 * 0.90 = 99.999 -> 100.00
    (1000.0, "premium", 900.0), # Large value
])
def test_value_over_100_premium_customer_gets_10_percent_discount(value, customer_type, expected_price):
    assert calculate_final_price(value, customer_type) == pytest.approx(expected_price)

# Additional rounding edge cases (Rule 4: rounded to 2 decimal places using Python's round half to even)
@pytest.mark.parametrize("value, customer_type, expected_price", [
    # Common customer (5% discount)
    # Result ends in .005 -> rounds to .00 (even)
    (100.00526315789474, "common", 95.00), # 100.00526315789474 * 0.95 = 95.005 -> round(95.005, 2) = 95.00
    # Result ends in .015 -> rounds to .02 (even)
    (100.01578947368421, "common", 95.02), # 100.01578947368421 * 0.95 = 95.015 -> round(95.015, 2) = 95.02

    # Premium customer (10% discount)
    # Result ends in .005 -> rounds to .00 (even)
    (100.00555555555556, "premium", 90.00), # 100.00555555555556 * 0.90 = 90.005 -> round(90.005, 2) = 90.00
    # Result ends in .015 -> rounds to .02 (even)
    (100.01666666666667, "premium", 90.02), # 100.01666666666667 * 0.90 = 90.015 -> round(90.015, 2) = 90.02
])
def test_rounding_edge_cases(value, customer_type, expected_price):
    assert calculate_final_price(value, customer_type) == pytest.approx(expected_price)
