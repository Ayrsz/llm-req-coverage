import pytest
from solution import final_balance

def test_final_balance_empty_operations_list():
    """
    Cenário 1: Lista de operações vazia.
    """
    initial = 100.0
    operations = []
    expected_result = 100.0
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_only_deposits():
    """
    Cenário 2: Apenas operações de depósito.
    """
    initial = 100.0
    operations = [("deposit", 50.0), ("deposit", 25.0)]
    expected_result = 175.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_sufficient_withdraw():
    """
    Cenário 3: Saque com saldo suficiente.
    """
    initial = 100.0
    operations = [("withdraw", 30.0)]
    expected_result = 70.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_insufficient_withdraw_ignored():
    """
    Cenário 4: Saque com saldo insuficiente (operação ignorada).
    """
    initial = 100.0
    operations = [("withdraw", 150.0)]
    expected_result = 100.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_withdraw_equal_to_balance():
    """
    Cenário 5: Saque exatamente igual ao saldo (valor-limite).
    """
    initial = 100.0
    operations = [("withdraw", 100.0)]
    expected_result = 0.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_withdraw_slightly_more_than_balance_ignored():
    """
    Cenário 6: Saque ligeiramente maior que o saldo (valor-limite, ignorado).
    """
    initial = 100.0
    operations = [("withdraw", 100.01)]
    expected_result = 100.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_unknown_operation_type_ignored():
    """
    Cenário 7: Operação com tipo desconhecido (ignorada).
    """
    initial = 100.0
    operations = [("bonus", 50.0)]
    expected_result = 100.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_mixed_operations_sequence():
    """
    Cenário 8: Sequência mista de operações, incluindo depósitos, saques suficientes e saques insuficientes.
    """
    initial = 100.0
    operations = [("deposit", 50.0), ("withdraw", 200.0), ("withdraw", 100.0)]
    expected_result = 50.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_zero_initial_with_deposit():
    """
    Cenário 9: Saldo inicial zero com depósito.
    """
    initial = 0.0
    operations = [("deposit", 10.0)]
    expected_result = 10.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_zero_initial_with_withdraw_ignored():
    """
    Cenário 10: Saldo inicial zero com saque (ignorada).
    """
    initial = 0.0
    operations = [("withdraw", 10.0)]
    expected_result = 0.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_deposit_zero_value():
    """
    Cenário 11: Operação de depósito com valor zero.
    """
    initial = 50.0
    operations = [("deposit", 0.0)]
    expected_result = 50.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_withdraw_zero_value():
    """
    Cenário 12: Operação de saque com valor zero.
    """
    initial = 50.0
    operations = [("withdraw", 0.0)]
    expected_result = 50.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_multiple_ignored_operations_consecutive():
    """
    Cenário 13: Múltiplas operações ignoradas consecutivamente.
    """
    initial = 20.0
    operations = [("withdraw", 30.0), ("unknown_type", 10.0), ("withdraw", 25.0)]
    expected_result = 20.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_final_balance_exactly_zero():
    """
    Cenário 14: Saldo final exatamente zero após múltiplas operações.
    """
    initial = 100.0
    operations = [("deposit", 50.0), ("withdraw", 100.0), ("withdraw", 50.0)]
    expected_result = 0.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_decimal_rounding_down():
    """
    Cenário 15: Operações com valores decimais que exigem arredondamento final para 2 casas (arredonda para baixo).
    """
    initial = 10.0
    operations = [("deposit", 3.333), ("withdraw", 1.111)]
    expected_result = 12.22
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_decimal_rounding_up():
    """
    Cenário 16: Operações com valores decimais que exigem arredondamento final para 2 casas (arredonda para cima).
    """
    initial = 10.0
    operations = [("deposit", 0.005)]
    expected_result = 10.01
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_mixed_numeric_types():
    """
    Cenário 17: Mistura de tipos numéricos (int e float) para `initial` e `valor`.
    """
    initial = 100
    operations = [("deposit", 50.5), ("withdraw", 20)]
    expected_result = 130.50
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_large_initial_balance():
    """
    Cenário 18: Saldo inicial muito grande.
    """
    initial = 1_000_000_000.0
    operations = [("deposit", 100.0)]
    expected_result = 1_000_000_100.00
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_withdraw_leaves_minimum_positive():
    """
    Cenário 19: Saque que deixa o saldo com um valor mínimo positivo.
    """
    initial = 10.0
    operations = [("withdraw", 9.99)]
    expected_result = 0.01
    assert final_balance(initial, operations) == pytest.approx(expected_result)

def test_final_balance_withdraw_slightly_more_than_minimum_ignored():
    """
    Cenário 20: Saque que deixaria o saldo com um valor mínimo positivo, mas é ignorado por ser ligeiramente maior.
    """
    initial = 0.01
    operations = [("withdraw", 0.02)]
    expected_result = 0.01
    assert final_balance(initial, operations) == pytest.approx(expected_result)
