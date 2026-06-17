import pytest
from solution import apply_commands

# Test cases for AC1: Empty commands list
@pytest.mark.parametrize("start_value, expected", [
    (0, 0),
    (1, 1),
    (100, 100),
])
def test_apply_commands_empty_list(start_value, expected):
    """
    AC1. Testa que uma lista de comandos vazia retorna o valor inicial.
    """
    assert apply_commands(start_value, []) == expected

# Test cases for AC2: Only "inc" commands
@pytest.mark.parametrize("start_value, commands, expected", [
    (0, ["inc"], 1),
    (0, ["inc", "inc", "inc"], 3),  # AC2
    (5, ["inc"], 6),
    (10, ["inc", "inc"], 12),
])
def test_apply_commands_only_inc(start_value, commands, expected):
    """
    AC2. Testa o comportamento com apenas comandos de incremento.
    """
    assert apply_commands(start_value, commands) == expected

# Test cases for AC3, AC4, AC5: Only "dec" commands, including floor at 0
@pytest.mark.parametrize("start_value, commands, expected", [
    (5, ["dec"], 4),
    (5, ["dec", "dec"], 3),  # AC3
    (1, ["dec"], 0),
    (0, ["dec"], 0),  # AC4: dec em 0 mantém 0 (fronteira)
    (1, ["dec", "dec"], 0),  # AC5: segundo dec não passa de 0 (piso)
    (2, ["dec", "dec", "dec"], 0), # dec abaixo de zero
    (10, ["dec", "dec", "dec", "dec", "dec", "dec", "dec", "dec", "dec", "dec", "dec"], 0), # muitos dec
])
def test_apply_commands_only_dec_with_floor(start_value, commands, expected):
    """
    AC3, AC4, AC5. Testa o comportamento com apenas comandos de decremento,
    incluindo o piso em 0.
    """
    assert apply_commands(start_value, commands) == expected

# Test cases for AC6: Only "double" commands
@pytest.mark.parametrize("start_value, commands, expected", [
    (3, ["double"], 6),  # AC6
    (0, ["double"], 0),  # Valor-limite: double em 0
    (1, ["double"], 2),
    (2, ["double", "double"], 8),
    (10, ["double", "double", "double"], 80),
])
def test_apply_commands_only_double(start_value, commands, expected):
    """
    AC6. Testa o comportamento com apenas comandos de dobrar.
    """
    assert apply_commands(start_value, commands) == expected

# Test cases for AC7: Only "reset" commands
@pytest.mark.parametrize("start_value, commands, expected", [
    (7, ["reset"], 0),  # AC7
    (0, ["reset"], 0),
    (100, ["reset"], 0),
])
def test_apply_commands_only_reset(start_value, commands, expected):
    """
    AC7. Testa o comportamento com apenas comandos de reset.
    """
    assert apply_commands(start_value, commands) == expected

# Test cases for AC8: Unknown commands
@pytest.mark.parametrize("start_value, commands, expected", [
    (4, ["spin", "inc"], 5),  # AC8: comando desconhecido ignorado
    (5, ["unknown_command"], 5),
    (10, ["inc", "invalid_cmd", "dec"], 10), # 10 -> inc (11) -> invalid (11) -> dec (10)
    (0, ["invalid", "double"], 0), # 0 -> invalid (0) -> double (0)
    (1, ["inc", "foo", "bar", "double", "baz", "dec"], 3), # 1 -> inc (2) -> foo (2) -> bar (2) -> double (4) -> baz (4) -> dec (3)
])
def test_apply_commands_unknown_commands_ignored(start_value, commands, expected):
    """
    AC8. Testa que comandos desconhecidos são ignorados e não alteram o contador.
    """
    assert apply_commands(start_value, commands) == expected

# Test cases for mixed commands, covering various scenarios and order of operations
@pytest.mark.parametrize("start_value, commands, expected", [
    # Mistura simples
    (5, ["inc", "double", "dec"], 11), # 5 -> inc (6) -> double (12) -> dec (11)
    (10, ["reset", "inc", "inc"], 2), # 10 -> reset (0) -> inc (1) -> inc (2)
    (1, ["double", "dec", "inc"], 2), # 1 -> double (2) -> dec (1) -> inc (2)

    # Cenários com piso em 0
    (5, ["dec", "dec", "dec", "dec", "dec", "dec", "inc"], 1), # 5 -> ... (0) -> inc (1)
    (10, ["double", "reset", "dec", "inc"], 1), # 10 -> double (20) -> reset (0) -> dec (0) -> inc (1)
    (0, ["inc", "dec", "double", "reset", "inc"], 1), # 0 -> inc (1) -> dec (0) -> double (0) -> reset (0) -> inc (1)

    # Cenários com comandos desconhecidos misturados
    (10, ["inc", "unknown", "double", "dec", "reset", "inc", "inc", "dec", "dec", "dec", "dec"], 0),
    # 10 -> inc (11) -> unknown (11) -> double (22) -> dec (21) -> reset (0) -> inc (1) -> inc (2) -> dec (1) -> dec (0) -> dec (0) -> dec (0)
    (5, ["inc", "foo", "double", "bar", "dec", "baz", "reset", "qux", "inc"], 1),
    # 5 -> inc (6) -> foo (6) -> double (12) -> bar (12) -> dec (11) -> baz (11) -> reset (0) -> qux (0) -> inc (1)

    # Valores iniciais diferentes
    (0, ["inc", "double", "dec"], 1), # 0 -> inc (1) -> double (2) -> dec (1)
    (100, ["reset", "inc", "double", "dec"], 1), # 100 -> reset (0) -> inc (1) -> double (2) -> dec (1)
])
def test_apply_commands_mixed_scenarios(start_value, commands, expected):
    """
    Testa uma mistura de comandos, incluindo casos típicos, de borda e com comandos desconhecidos.
    """
    assert apply_commands(start_value, commands) == expected

# Teste de invariante: o contador nunca fica abaixo de 0
@pytest.mark.parametrize("start_value, commands, expected", [
    (0, ["dec"], 0),
    (1, ["dec", "dec"], 0),
    (10, ["dec"] * 20, 0), # Muitos decrementos
    (5, ["dec", "double", "dec", "dec", "dec", "dec", "dec", "dec"], 0), # 5 -> dec (4) -> double (8) -> dec (7) -> ... -> 0
])
def test_apply_commands_invariants_never_below_zero(start_value, commands, expected):
    """
    Verifica o invariante de que o contador nunca fica abaixo de 0.
    """
    assert apply_commands(start_value, commands) == expected

# Teste com lista de comandos muito longa
@pytest.mark.parametrize("start_value, commands, expected", [
    (0, ["inc"] * 1000, 1000),
    (1000, ["dec"] * 2000, 0),
    (1, ["double"] * 10, 1024), # 1 * 2^10
    (100, ["reset", "inc"] * 500, 1), # 100 -> reset (0) -> inc (1) -> reset (0) -> inc (1) ...
])
def test_apply_commands_long_list_of_commands(start_value, commands, expected):
    """
    Testa o comportamento com uma lista de comandos muito longa.
    """
    assert apply_commands(start_value, commands) == expected

# Teste com valores de start grandes
@pytest.mark.parametrize("start_value, commands, expected", [
    (1_000_000, [], 1_000_000),
    (1_000_000, ["inc"], 1_000_001),
    (1_000_000, ["dec"], 999_999),
    (1_000_000, ["double"], 2_000_000),
    (1_000_000, ["reset"], 0),
    (1_000_000, ["inc", "double", "dec", "reset", "inc"], 1),
])
def test_apply_commands_large_start_value(start_value, commands, expected):
    """
    Testa o comportamento com um valor inicial de contador grande.
    """
    assert apply_commands(start_value, commands) == expected
