from solution import validate_password
import pytest

# Testes para senhas válidas (devem retornar True)
@pytest.mark.parametrize("password", [
    "Abcdef1!",          # AC1 - Típico, 8 caracteres, todas as regras
    "MyStrongP@ssw0rd!", # Mais longa, todas as regras
    "A1b2C3d4!",         # Exatamente 8 caracteres, todas as regras (valor-limite)
    "P@ssw0rd123ABC",    # Outra senha válida
    "aB1!cDeF",          # Exatamente 8 caracteres, ordem diferente
    "Teste123@",         # Mais um caso válido
])
def test_validate_password_valid(password):
    """
    Verifica que senhas que atendem a todas as regras são consideradas válidas.
    """
    assert validate_password(password) is True

# Testes para senhas inválidas (devem retornar False)
@pytest.mark.parametrize("password", [
    # Casos de comprimento
    "Abc1!",             # AC2 - Curta demais (5 caracteres)
    "Abcde1!",           # 7 caracteres, senão tudo certo (valor-limite)
    "",                  # AC7 - Vazia

    # Casos de falta de caractere específico (uma falha por vez)
    "abcdef1!",          # AC3 - Sem maiúscula
    "ABCDEF1!",          # AC4 - Sem minúscula
    "Abcdefg!",          # AC5 - Sem dígito
    "Abcdefg1",          # AC6 - Sem símbolo

    # Casos com múltiplas falhas
    "abc",               # Curta, sem maiúscula, sem dígito, sem símbolo
    "ABC",               # Curta, sem minúscula, sem dígito, sem símbolo
    "1234567",           # Curta, sem letras, sem símbolo
    "password",          # Sem maiúscula, sem dígito, sem símbolo
    "PASSWORD",          # Sem minúscula, sem dígito, sem símbolo
    "12345678",          # Sem letras, sem símbolo
    "!@#$%^&*",          # Sem letras, sem dígitos
    "Abcdef",            # Curta, sem dígito, sem símbolo
    "Abcdefg",           # Curta, sem dígito, sem símbolo
    "Abcdefgh",          # 8 caracteres, mas sem dígito e sem símbolo
    "AbcdefgH",          # 8 caracteres, mas sem dígito e sem símbolo
    "123456789",         # 9 caracteres, mas sem letras e sem símbolo
    "abcdefgh!",         # 9 caracteres, mas sem maiúscula e sem dígito
])
def test_validate_password_invalid(password):
    """
    Verifica que senhas que falham em uma ou mais regras são consideradas inválidas.
    """
    assert validate_password(password) is False
