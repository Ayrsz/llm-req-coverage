import pytest
from solution import apply_commands

# 1. Cenários para Lista de Comandos Vazia
@pytest.mark.parametrize("start, commands, expected", [
    (5, [], 5),  # Cenário: start=5, commands=[] -> 5
    (0, [], 0),  # Cenário: start=0, commands=[] -> 0
])
def test_empty_commands_list(start: int, commands: list, expected: int):
    """Testa o comportamento com uma lista de comandos vazia."""
    assert apply_commands(start, commands) == expected

# 2. Cenários para Comandos Individuais
@pytest.mark.parametrize("start, commands, expected", [
    # 2.1. Comando "inc"
    (5, ["inc"], 6),  # Cenário: start=5, commands=["inc"] -> 6
    # 2.2. Comando "dec"
    (5, ["dec"], 4),  # Cenário: start=5, commands=["dec"] -> 4
    (1, ["dec"], 0),  # Cenário: start=1, commands=["dec"] -> 0 (limite)
    (0, ["dec"], 0),  # Cenário: start=0, commands=["dec"] -> 0 (piso)
    # 2.3. Comando "double"
    (3, ["double"], 6),  # Cenário: start=3, commands=["double"] -> 6
    (0, ["double"], 0),  # Cenário: start=0, commands=["double"] -> 0
    # 2.4. Comando "reset"
    (7, ["reset"], 0),  # Cenário: start=7, commands=["reset"] -> 0
    (0, ["reset"], 0),  # Cenário: start=0, commands=["reset"] -> 0
    # 2.5. Comando Desconhecido
    (10, ["unknown_command"], 10),  # Cenário: start=10, commands=["unknown_command"] -> 10
])
def test_single_commands(start: int, commands: list, expected: int):
    """Testa o comportamento com comandos individuais."""
    assert apply_commands(start, commands) == expected

# 3. Cenários para Sequências de Comandos (incluindo mistos e complexos)
@pytest.mark.parametrize("start, commands, expected", [
    # 3.1. Sequência de Incrementos
    (0, ["inc", "inc", "inc"], 3),  # Cenário: start=0, commands=["inc", "inc", "inc"] -> 3
    # 3.2. Sequência de Decrementos com Folga
    (5, ["dec", "dec"], 3),  # Cenário: start=5, commands=["dec", "dec"] -> 3
    # 3.3. Sequência de Decrementos Atingindo o Piso (0)
    (1, ["dec", "dec"], 0),  # Cenário: start=1, commands=["dec", "dec"] -> 0
    (2, ["dec", "dec", "dec"], 0),  # Cenário: start=2, commands=["dec", "dec", "dec"] -> 0
    # 3.4. Sequência com Comando Desconhecido
    (4, ["spin", "inc"], 5),  # Cenário: start=4, commands=["spin", "inc"] -> 5
    (10, ["unknown1", "inc", "unknown2", "dec"], 10),  # Cenário: start=10, commands=["unknown1", "inc", "unknown2", "dec"] -> 10
    # 3.5. Sequências Mistas e Complexas
    (5, ["inc", "double", "dec", "reset", "inc"], 1),  # Cenário: start=5, commands=["inc", "double", "dec", "reset", "inc"] -> 1
    (10, ["double", "reset", "inc", "dec", "double"], 0),  # Cenário: start=10, commands=["double", "reset", "inc", "dec", "double"] -> 0
    (1, ["dec", "double", "inc"], 1),  # Cenário: start=1, commands=["dec", "double", "inc"] -> 1
    (0, ["inc", "double", "dec", "dec", "inc"], 1),  # Cenário: start=0, commands=["inc", "double", "dec", "dec", "inc"] -> 1
    # 4. Cenários de Borda e Invariantes Específicos
    # 4.1. Valor Inicial do Contador (start) - start grande
    (1000, ["inc", "dec", "double", "reset"], 0),  # Cenário: start=1000, commands=["inc", "dec", "double", "reset"] -> 0
    # 4.2. Invariante: Contador Nunca Negativo (Sequência Extensa)
    (0, ["dec", "dec", "inc", "dec", "dec"], 0),  # Cenário: start=0, commands=["dec", "dec", "inc", "dec", "dec"] -> 0
])
def test_command_sequences(start: int, commands: list, expected: int):
    """Testa o comportamento com sequências de comandos, incluindo mistos e casos de borda."""
    assert apply_commands(start, commands) == expected
