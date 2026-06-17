import pytest
from solution import final_balance


def test_ac1_empty_operations_list():
    # AC1. final_balance(100.0, []) == 100.0 (lista vazia retorna inicial).
    assert final_balance(100.0, []) == pytest.approx(100.0)


def test_ac2_single_deposit():
    # AC2. final_balance(100.0, [("deposit", 50.0)]) == 150.0 (depósito soma).
    assert final_balance(100.0, [("deposit", 50.0)]) == pytest.approx(150.0)


def test_ac3_sufficient_withdraw():
    # AC3. final_balance(100.0, [("withdraw", 30.0)]) == 70.0 (saque com saldo suficiente).
    assert final_balance(100.0, [("withdraw", 30.0)]) == pytest.approx(70.0)


def test_ac4_insufficient_withdraw_ignored():
    # AC4. final_balance(100.0, [("withdraw", 150.0)]) == 100.0 (saque insuficiente ignorado).
    assert final_balance(100.0, [("withdraw", 150.0)]) == pytest.approx(100.0)


def test_ac5_withdraw_equal_to_balance_goes_to_zero():
    # AC5. final_balance(100.0, [("withdraw", 100.0)]) == 0.0 (fronteira: saque igual ao saldo, vai a 0).
    assert final_balance(100.0, [("withdraw", 100.0)]) == pytest.approx(0.0)


def test_ac6_unknown_operation_type_ignored():
    # AC6. final_balance(100.0, [("bonus", 50.0)]) == 100.0 (tipo desconhecido ignorado).
    assert final_balance(100.0, [("bonus", 50.0)]) == pytest.approx(100.0)


def test_ac7_mixed_operations_with_ignored_withdraw():
    # AC7. final_balance(100.0, [("deposit", 50.0), ("withdraw", 200.0), ("withdraw", 100.0)]) == 50.0
    # (ordem; 1º saque ignorado, 2º efetivado).
    operations = [("deposit", 50.0), ("withdraw", 200.0), ("withdraw", 100.0)]
    assert final_balance(100.0, operations) == pytest.approx(50.0)


@pytest.mark.parametrize("initial, expected", [
    (0.0, 0.0),
    (123.45, 123.45),
])
def test_empty_operations_list_various_initial_balances(initial, expected):
    assert final_balance(initial, []) == pytest.approx(expected)


@pytest.mark.parametrize("initial, operations, expected", [
    (0.0, [("deposit", 10.0)], 10.0),
    (50.0, [("deposit", 0.0)], 50.0),  # Deposit zero
    (10.0, [("deposit", 5.5), ("deposit", 2.25)], 17.75),  # Multiple deposits
    (10.0, [("deposit", 0.001)], 10.00),  # Deposit small value, rounding down
    (10.0, [("deposit", 0.005)], 10.01),  # Deposit small value, rounding up
    (10.0, [("deposit", 0.0049)], 10.00),  # Deposit small value, rounding down
    (10.0, [("deposit", 0.0051)], 10.01),  # Deposit small value, rounding up
])
def test_deposits_scenarios(initial, operations, expected):
    assert final_balance(initial, operations) == pytest.approx(expected)


@pytest.mark.parametrize("initial, operations, expected", [
    (10.0, [("withdraw", 0.0)], 10.0),  # Withdraw zero
    (100.0, [("withdraw", 50.0), ("withdraw", 20.0)], 30.0),  # Multiple sufficient withdrawals
    (0.0, [("withdraw", 0.0)], 0.0),  # Withdraw zero from zero balance
    (10.0, [("withdraw", 0.001)], 10.00),  # Withdraw small value, rounding down
    (10.0, [("withdraw", 0.005)], 9.99),  # Withdraw small value, rounding up
    (10.0, [("withdraw", 0.0049)], 10.00),  # Withdraw small value, rounding down
    (10.0, [("withdraw", 0.0051)], 9.99),  # Withdraw small value, rounding up
])
def test_sufficient_withdrawals_scenarios(initial, operations, expected):
    assert final_balance(initial, operations) == pytest.approx(expected)


@pytest.mark.parametrize("initial, operations, expected", [
    (10.0, [("withdraw", 10.01)], 10.0),  # Just over balance
    (10.0, [("withdraw", 100.0)], 10.0),  # Much over balance
    (0.0, [("withdraw", 0.01)], 0.0),  # Withdraw from zero balance
    (0.0, [("withdraw", 100.0)], 0.0),  # Withdraw from zero balance
    (100.0, [("withdraw", 50.0), ("withdraw", 60.0)], 50.0),  # First sufficient, second insufficient
])
def test_insufficient_withdrawals_scenarios(initial, operations, expected):
    assert final_balance(initial, operations) == pytest.approx(expected)


@pytest.mark.parametrize("initial, operations, expected", [
    (100.0, [("unknown", 10.0)], 100.0),
    (100.0, [("deposit", 10.0), ("unknown", 50.0), ("withdraw", 5.0)], 105.0),  # Mixed with valid
    (100.0, [("unknown", 0.0)], 100.0),  # Unknown type with zero value
    (100.0, [("deposit", 10.0), ("withdraw", 1000.0), ("unknown", 50.0)], 110.0),  # Unknown after insufficient withdraw
    (100.0, [("deposit", 10.0), ("deposit", 20.0), ("invalid_op", 5.0), ("withdraw", 15.0)], 115.0),
])
def test_unknown_operation_types_ignored(initial, operations, expected):
    assert final_balance(initial, operations) == pytest.approx(expected)


@pytest.mark.parametrize("initial, operations, expected", [
    # Deposit, then withdraw more than current balance, then withdraw less than current balance
    (100.0, [("deposit", 50.0), ("withdraw", 200.0), ("withdraw", 30.0)], 120.0),
    # Withdraw, then deposit, then withdraw more than current balance
    (100.0, [("withdraw", 20.0), ("deposit", 10.0), ("withdraw", 100.0)], 90.0),
    # All types of operations in a sequence
    (50.0, [("deposit", 20.0), ("withdraw", 30.0), ("bonus", 100.0), ("withdraw", 50.0), ("deposit", 5.0)], 45.0),
    # Operations with float values
    (10.50, [("deposit", 2.75), ("withdraw", 5.25)], 8.00),
    # Operations leading to zero and then trying to withdraw
    (100.0, [("withdraw", 100.0), ("withdraw", 10.0)], 0.0),
    # Operations with very small values and rounding
    (0.0, [("deposit", 0.004), ("deposit", 0.004), ("deposit", 0.004)], 0.01),  # 0.0 + 0.012 -> 0.01
    (0.0, [("deposit", 0.005), ("deposit", 0.005), ("deposit", 0.005)], 0.02),  # 0.0 + 0.015 -> 0.02
    (100.0, [("withdraw", 0.005), ("withdraw", 0.005), ("withdraw", 0.005)], 99.98),  # 100.0 - 0.015 -> 99.98
    (100.0, [("withdraw", 0.004), ("withdraw", 0.004), ("withdraw", 0.004)], 99.99),  # 100.0 - 0.012 -> 99.99
    (10.0, [("deposit", 0.0000000000000001)], 10.00), # Very small deposit, rounds to 0
])
def test_complex_sequences_and_rounding(initial, operations, expected):
    assert final_balance(initial, operations) == pytest.approx(expected)


def test_initial_balance_as_int():
    assert final_balance(100, [("deposit", 50)]) == pytest.approx(150.0)
    assert final_balance(100, [("withdraw", 30)]) == pytest.approx(70.0)


def test_operation_value_as_int():
    assert final_balance(100.0, [("deposit", 50)]) == pytest.approx(150.0)
    assert final_balance(100.0, [("withdraw", 30)]) == pytest.approx(70.0)


def test_mixed_int_float_values():
    assert final_balance(100, [("deposit", 50.5), ("withdraw", 20)]) == pytest.approx(130.5)
    assert final_balance(100.5, [("deposit", 50), ("withdraw", 20.5)]) == pytest.approx(130.0)


def test_large_numbers():
    assert final_balance(1_000_000.0, [("deposit", 500_000.0), ("withdraw", 200_000.0)]) == pytest.approx(1_300_000.0)
    assert final_balance(1_000_000.0, [("withdraw", 1_500_000.0)]) == pytest.approx(1_000_000.0)


@pytest.mark.parametrize("operations, expected", [
    ([], 0.0),
    ([("deposit", 10.0)], 10.0),
    ([("withdraw", 5.0)], 0.0),  # Insufficient
    ([("deposit", 5.0), ("withdraw", 5.0)], 0.0),
    ([("deposit", 5.0), ("withdraw", 10.0)], 5.0),  # Insufficient
    ([("unknown", 10.0)], 0.0),
])
def test_zero_initial_balance_scenarios(operations, expected):
    assert final_balance(0.0, operations) == pytest.approx(expected)
