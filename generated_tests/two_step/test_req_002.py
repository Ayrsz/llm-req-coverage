from solution import validate_password
import pytest

# 1. Cenários de Validação Positiva (Senha Válida)

def test_validate_password_valid_min_length():
    """
    Cenário 1.1: Senha válida com comprimento mínimo e todos os tipos de caracteres.
    Entrada: "Abcdef1!"
    Resultado Esperado: True
    """
    assert validate_password("Abcdef1!") is True

def test_validate_password_valid_longer_length():
    """
    Cenário 1.2: Senha válida com comprimento maior que o mínimo e todos os tipos de caracteres.
    Entrada: "MinhaSenhaForte123!"
    Resultado Esperado: True
    """
    assert validate_password("MinhaSenhaForte123!") is True

def test_validate_password_valid_multiple_char_types():
    """
    Cenário 1.3: Senha válida com múltiplos caracteres de cada tipo.
    Entrada: "MuitoF0rte!@#$"
    Resultado Esperado: True
    """
    assert validate_password("MuitoF0rte!@#$") is True

def test_validate_password_valid_with_space_symbol():
    """
    Cenário 1.4: Senha válida contendo espaço como um dos símbolos.
    Entrada: "Senha Com Espaco 1!"
    Resultado Esperado: True
    """
    assert validate_password("Senha Com Espaco 1!") is True

def test_validate_password_valid_symbol_start_end():
    """
    Cenário 1.5: Senha válida com símbolos em diferentes posições (início e fim).
    Entrada: "!Abcdef1@"
    Resultado Esperado: True
    """
    assert validate_password("!Abcdef1@") is True

def test_validate_password_valid_symbol_middle():
    """
    Cenário 1.5: Senha válida com símbolos em diferentes posições (meio).
    Entrada: "Abc!def1@"
    Resultado Esperado: True
    """
    assert validate_password("Abc!def1@") is True

def test_validate_password_valid_uncommon_symbol_tilde():
    """
    Cenário 1.6: Senha válida com símbolos ASCII imprimíveis menos comuns (ex: ~).
    Entrada: "Abcdef1~"
    Resultado Esperado: True
    """
    assert validate_password("Abcdef1~") is True

def test_validate_password_valid_uncommon_symbol_underscore():
    """
    Cenário 1.6: Senha válida com símbolos ASCII imprimíveis menos comuns (ex: _).
    Entrada: "Abcdef1_"
    Resultado Esperado: True
    """
    assert validate_password("Abcdef1_") is True

# 2. Cenários de Validação Negativa (Senha Inválida - Falha em uma única regra)

def test_validate_password_empty():
    """
    Cenário 2.1: Senha vazia.
    Entrada: ""
    Resultado Esperado: False
    """
    assert validate_password("") is False

def test_validate_password_invalid_length_boundary():
    """
    Cenário 2.2: Senha com 7 caracteres (comprimento limite inferior inválido),
    mas com todos os outros tipos de caracteres presentes.
    Entrada: "Abcde1!"
    Resultado Esperado: False
    """
    assert validate_password("Abcde1!") is False

def test_validate_password_invalid_too_short():
    """
    Cenário 2.3: Senha muito curta (5 caracteres), falhando na regra de comprimento.
    Entrada: "Abc1!"
    Resultado Esperado: False
    """
    assert validate_password("Abc1!") is False

def test_validate_password_invalid_no_uppercase():
    """
    Cenário 2.4: Senha sem letra maiúscula.
    Entrada: "abcdef1!"
    Resultado Esperado: False
    """
    assert validate_password("abcdef1!") is False

def test_validate_password_invalid_no_lowercase():
    """
    Cenário 2.5: Senha sem letra minúscula.
    Entrada: "ABCDEF1!"
    Resultado Esperado: False
    """
    assert validate_password("ABCDEF1!") is False

def test_validate_password_invalid_no_digit():
    """
    Cenário 2.6: Senha sem dígito.
    Entrada: "Abcdefg!"
    Resultado Esperado: False
    """
    assert validate_password("Abcdefg!") is False

def test_validate_password_invalid_no_symbol():
    """
    Cenário 2.7: Senha sem símbolo.
    Entrada: "Abcdefg1"
    Resultado Esperado: False
    """
    assert validate_password("Abcdefg1") is False

# 3. Cenários de Validação Negativa (Senha Inválida - Falha em Múltiplas Regras ou Casos de Borda)

def test_validate_password_invalid_short_no_uppercase():
    """
    Cenário 3.1: Senha muito curta E sem letra maiúscula.
    Entrada: "abcde1!"
    Resultado Esperado: False
    """
    assert validate_password("abcde1!") is False

def test_validate_password_invalid_all_types_but_too_short():
    """
    Cenário 3.2: Senha com o mínimo de cada tipo de caractere (maiúscula, minúscula, dígito, símbolo),
    mas não o comprimento mínimo.
    Entrada: "A1a!" (4 caracteres)
    Resultado Esperado: False
    """
    assert validate_password("A1a!") is False

def test_validate_password_invalid_only_lowercase():
    """
    Cenário 3.3: Senha longa o suficiente, mas contendo apenas minúsculas.
    Entrada: "aaaaaaaaa" (9 caracteres, só minúsculas)
    Resultado Esperado: False
    """
    assert validate_password("aaaaaaaaa") is False

def test_validate_password_invalid_only_uppercase():
    """
    Cenário 3.3: Senha longa o suficiente, mas contendo apenas maiúsculas.
    Entrada: "AAAAAAAAA" (9 caracteres, só maiúsculas)
    Resultado Esperado: False
    """
    assert validate_password("AAAAAAAAA") is False

def test_validate_password_invalid_only_digits():
    """
    Cenário 3.3: Senha longa o suficiente, mas contendo apenas dígitos.
    Entrada: "111111111" (9 caracteres, só dígitos)
    Resultado Esperado: False
    """
    assert validate_password("111111111") is False

def test_validate_password_invalid_only_spaces():
    """
    Cenário 3.4: Senha longa o suficiente, contendo apenas espaços (considerados símbolos).
    Entrada: "        " (8 espaços, falha em maiúscula, minúscula, dígito)
    Resultado Esperado: False
    """
    assert validate_password("        ") is False
