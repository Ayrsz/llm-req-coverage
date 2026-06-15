import pytest
from solution import calculate_final_price
from decimal import Decimal, ROUND_HALF_UP

# Helper function to calculate expected values with round_half_up
# This function is for test purposes only to ensure correct expected values.
def _round_half_up(value):
    return float(Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

# Test cases for negative 'value' (invalid input)
def test_negative_value_returns_zero():
    """
    Test cases where the input 'value' is negative.
    According to rule 1 and AC4, the final price should be 0.0.
    """
    assert calculate_final_price(-0.01, "common") == 0.0
    assert calculate_final_price(-50.0, "common") == 0.0
    assert calculate_final_price(-100.0, "premium") == 0.0
    assert calculate_final_price(-0.0001, "common") == 0.0
    # AC4
    assert calculate_final_price(-50, "common") == 0.0

# Test cases for 'value' up to 100 (no discount applied)
def test_value_up_to_100_no_discount():
    """
    Test cases where 'value' is between 0 and 100 (inclusive).
    According to rule 2, no discount should be applied.
    The final price should be the 'value' itself, rounded to 2 decimal places.
    """
    # Edge cases
    assert calculate_final_price(0.0, "common") == 0.0
    assert calculate_final_price(0.0, "premium") == 0.0
    assert calculate_final_price(100.0, "common") == 100.0  # AC1
    assert calculate_final_price(100.0, "premium") == 100.0

    # Typical cases within range
    assert calculate_final_price(50.0, "common") == 50.0
    assert calculate_final_price(75.50, "premium") == 75.50
    assert calculate_final_price(1.0, "common") == 1.0

    # Rounding for values in this range (as per rule 4 and example 95.015 -> 95.02)
    assert calculate_final_price(95.015, "common") == pytest.approx(95.02)
    assert calculate_final_price(95.015, "premium") == pytest.approx(95.02)
    assert calculate_final_price(99.995, "common") == pytest.approx(100.00)
    assert calculate_final_price(99.994, "common") == pytest.approx(99.99)
    assert calculate_final_price(0.005, "common") == pytest.approx(0.01)
    assert calculate_final_price(0.004, "common") == pytest.approx(0.00)

# Test cases for 'value' above 100 with "common" customer type (5% discount)
def test_value_above_100_common_customer_5_percent_discount():
    """
    Test cases where 'value' is greater than 100 and 'customer_type' is "common".
    According to rule 3, a 5% discount should be applied, and the result rounded.
    """
    # Edge case: just above 100
    assert calculate_final_price(100.01, "common") == pytest.approx(_round_half_up(100.01 * 0.95)) # 95.0095 -> 95.01
    assert calculate_final_price(100.005, "common") == pytest.approx(_round_half_up(100.005 * 0.95)) # 95.00475 -> 95.00

    # Typical cases
    assert calculate_final_price(200.0, "common") == pytest.approx(190.0)  # AC2
    assert calculate_final_price(150.0, "common") == pytest.approx(142.50)

    # Rounding specific cases (as per rule 4 and example 142.975 -> 142.98, but after discount)
    assert calculate_final_price(142.975, "common") == pytest.approx(_round_half_up(142.975 * 0.95)) # 135.82625 -> 135.83
    assert calculate_final_price(105.263, "common") == pytest.approx(_round_half_up(105.263 * 0.95)) # 99.99985 -> 100.00
    assert calculate_final_price(100.015, "common") == pytest.approx(_round_half_up(100.015 * 0.95)) # 95.01425 -> 95.01
    assert calculate_final_price(100.025, "common") == pytest.approx(_round_half_up(100.025 * 0.95)) # 95.02375 -> 95.02
    assert calculate_final_price(100.035, "common") == pytest.approx(_round_half_up(100.035 * 0.95)) # 95.03325 -> 95.03
    assert calculate_final_price(100.045, "common") == pytest.approx(_round_half_up(100.045 * 0.95)) # 95.04275 -> 95.04
    assert calculate_final_price(100.055, "common") == pytest.approx(_round_half_up(100.055 * 0.95)) # 95.05225 -> 95.05

# Test cases for 'value' above 100 with "premium" customer type (10% discount)
def test_value_above_100_premium_customer_10_percent_discount():
    """
    Test cases where 'value' is greater than 100 and 'customer_type' is "premium".
    According to rule 3, a 10% discount should be applied, and the result rounded.
    """
    # Edge case: just above 100
    assert calculate_final_price(100.01, "premium") == pytest.approx(_round_half_up(100.01 * 0.90)) # 90.009 -> 90.01
    assert calculate_final_price(100.005, "premium") == pytest.approx(_round_half_up(100.005 * 0.90)) # 90.0045 -> 90.00

    # Typical cases
    assert calculate_final_price(200.0, "premium") == pytest.approx(180.0)  # AC3
    assert calculate_final_price(150.0, "premium") == pytest.approx(135.0)

    # Rounding specific cases
    assert calculate_final_price(142.975, "premium") == pytest.approx(_round_half_up(142.975 * 0.90)) # 128.6775 -> 128.68
    assert calculate_final_price(100.015, "premium") == pytest.approx(_round_half_up(100.015 * 0.90)) # 90.0135 -> 90.01
    assert calculate_final_price(100.025, "premium") == pytest.approx(_round_half_up(100.025 * 0.90)) # 90.0225 -> 90.02
    assert calculate_final_price(100.035, "premium") == pytest.approx(_round_half_up(100.035 * 0.90)) # 90.0315 -> 90.03
    assert calculate_final_price(100.045, "premium") == pytest.approx(_round_half_up(100.045 * 0.90)) # 90.0405 -> 90.04
    assert calculate_final_price(100.055, "premium") == pytest.approx(_round_half_up(100.055 * 0.90)) # 90.0495 -> 90.05

# Test cases for unknown 'customer_type' (treated as "common")
def test_unknown_customer_type_treated_as_common():
    """
    Test cases where 'customer_type' is not "common" or "premium".
    According to the domain, it should be treated as "common" (5% discount if value > 100).
    """
    assert calculate_final_price(200.0, "desconhecido") == pytest.approx(190.0)  # AC5
    assert calculate_final_price(150.0, "guest") == pytest.approx(142.50)
    assert calculate_final_price(100.01, "unknown") == pytest.approx(_round_half_up(100.01 * 0.95)) # 95.0095 -> 95.01
    assert calculate_final_price(142.975, "invalid_type") == pytest.approx(_round_half_up(142.975 * 0.95)) # 135.82625 -> 135.83
    assert calculate_final_price(100.0, "unknown") == 100.0 # No discount if value <= 100
    assert calculate_final_price(50.0, "invalid_type") == 50.0 # No discount if value <= 100

# Test cases for zero value with different customer types
def test_zero_value():
    """
    Test cases for value = 0.0.
    Should return 0.0 regardless of customer type.
    """
    assert calculate_final_price(0.0, "common") == 0.0
    assert calculate_final_price(0.0, "premium") == 0.0
    assert calculate_final_price(0.0, "unknown") == 0.0
