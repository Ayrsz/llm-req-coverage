import pytest
from solution import is_valid_ipv4

@pytest.mark.parametrize("ipv4_string", [
    "0.0.0.0",                  # AC1: Mínimo válido
    "255.255.255.255",          # AC2: Máximo válido
    "192.168.0.1",              # AC11: Caso típico
    "127.0.0.1",                # Loopback
    "10.0.0.1",                 # Faixa privada
    "1.2.3.4",                  # Simples e válido
    "0.1.2.3",                  # Octeto '0' no início
    "1.0.2.3",                  # Octeto '0' no meio
    "1.2.0.3",                  # Octeto '0' no meio
    "1.2.3.0",                  # Octeto '0' no final
    "255.0.0.0",                # Primeiro octeto máximo, outros mínimos
    "0.255.0.0",                # Segundo octeto máximo
    "0.0.255.0",                # Terceiro octeto máximo
    "0.0.0.255",                # Quarto octeto máximo
    "100.100.100.100",          # Octetos com três dígitos
    "1.1.1.1",                  # Todos uns
])
def test_valid_ipv4_addresses(ipv4_string):
    """
    Verifica endereços IPv4 sintaticamente válidos.
    """
    assert is_valid_ipv4(ipv4_string) is True

@pytest.mark.parametrize("ipv4_string", [
    "",                         # AC10: String vazia
    " ",                        # String com apenas espaço
    "   ",                      # String com múltiplos espaços
    "1.2.3",                    # AC6: Menos de 4 octetos (3)
    "1.2",                      # Menos de 4 octetos (2)
    "1",                        # Menos de 4 octetos (1)
    "1.2.3.4.5",                # AC7: Mais de 4 octetos (5)
    "1.2.3.4.5.6",              # Mais de 4 octetos (6)
    "1.2.3.",                   # AC8: Octeto vazio no final (ponto no final)
    ".1.2.3.4",                 # Octeto vazio no início (ponto no início)
    "1..2.3.4",                 # Octeto vazio no meio (pontos consecutivos)
    "1.2..3.4",                 # Octeto vazio no meio
    "1.2.3..4",                 # Octeto vazio no meio
    "...",                      # Apenas pontos
    "1234567890",               # Sem pontos, string longa
    "1.2.3.256",                # AC3: Valor do octeto muito alto (256)
    "256.0.0.0",                # Valor do octeto muito alto (256)
    "999.999.999.999",          # Todos os octetos muito altos
    "1.2.3.-1",                 # Caractere não-dígito (sinal de menos)
    "1.2.3.a",                  # AC9: Caractere não-dígito (letra)
    "a.b.c.d",                  # Todos os octetos com caracteres não-dígitos
    "1.2.3. 4",                 # Espaço dentro do octeto
    "1.2.3.4 ",                 # Espaço no final da string
    " 1.2.3.4",                 # Espaço no início da string
    "1.2.3.4\n",                # Caractere de nova linha
    "1.2.3.+4",                 # Caractere não-dígito (sinal de mais)
    "1.2.3.*",                  # Caractere especial
    "01.2.3.4",                 # AC4: Zero à esquerda no primeiro octeto
    "1.02.3.4",                 # Zero à esquerda no segundo octeto
    "1.2.03.4",                 # Zero à esquerda no terceiro octeto
    "1.2.3.04",                 # Zero à esquerda no quarto octeto
    "00.0.0.0",                 # AC5: Zero à esquerda ("00")
    "007.0.0.0",                # Zero à esquerda ("007")
    "010.0.0.0",                # Zero à esquerda ("010")
    "1.2.3.00",                 # Zero à esquerda ("00")
    "1.2.3.000",                # Zero à esquerda ("000")
    "0.0.0.00",                 # Zero à esquerda ("00") mesmo para valor 0
    "1.2.3.256.5",              # Múltiplas falhas: valor fora da faixa e muitos octetos
    "1.2.3.a.5",                # Múltiplas falhas: não-dígito e muitos octetos
    "1.2.3.01.5",               # Múltiplas falhas: zero à esquerda e muitos octetos
    "1.2.3.255.",               # Octeto válido, mas ponto final
    "1.2.3.255..",              # Octeto válido, mas pontos consecutivos no final
    "1.2.3.255\t",              # Caractere de tabulação no final
    "1.2.3.255\r",              # Caractere de retorno de carro no final
    "1.2.3.255\x00",            # Caractere nulo no final
    "1.2.3.255\u2000",          # Espaço Unicode no final
])
def test_invalid_ipv4_addresses(ipv4_string):
    """
    Verifica endereços IPv4 sintaticamente inválidos.
    """
    assert is_valid_ipv4(ipv4_string) is False
