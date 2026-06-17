import pytest
from solution import is_valid_ipv4

class TestIsValidIPv4:

    # A. Cenários Válidos (Classe de Equivalência: IPv4 canônico bem-formado)
    @pytest.mark.parametrize("ipv4_string", [
        "0.0.0.0",             # 1. Análise de Valores-Limite (Mínimo)
        "255.255.255.255",     # 2. Análise de Valores-Limite (Máximo)
        "192.168.0.1",         # 3. Classe de Equivalência (Caso Típico)
        "1.10.100.255",        # 4. Classe de Equivalência (Octetos com 1, 2 e 3 dígitos)
        "10.0.200.5",          # 5. Classe de Equivalência (Octetos com zero válido)
    ])
    def test_valid_ipv4_addresses(self, ipv4_string):
        assert is_valid_ipv4(ipv4_string) is True

    # B. Cenários Inválidos - Número de Octetos (Viola Regra 1)
    @pytest.mark.parametrize("ipv4_string", [
        "1.2.3",               # 6. Menos de 4 octetos
        "1.2.3.4.5",           # 7. Mais de 4 octetos
        "127",                 # 8. Apenas um octeto
        "1.2",                 # Dois octetos
        "1",                   # Um octeto
    ])
    def test_invalid_ipv4_wrong_number_of_octets(self, ipv4_string):
        assert is_valid_ipv4(ipv4_string) is False

    # C. Cenários Inválidos - Octetos Vazios / Pontos Mal Posicionados (Viola Regra 1)
    @pytest.mark.parametrize("ipv4_string", [
        ".1.2.3.4",            # 9. Ponto inicial
        "1.2.3.4.",            # 10. Ponto final
        "1.2..3.4",            # 11. Pontos consecutivos / octeto vazio no meio
        "... ",                # 12. Apenas pontos (e espaço)
        "...",                 # Apenas pontos (sem espaço)
        "1..2..3..4",          # Múltiplos octetos vazios
        "1.2.3..",             # Ponto final e octeto vazio
        "..1.2.3.4",           # Múltiplos pontos iniciais
    ])
    def test_invalid_ipv4_empty_or_misplaced_octets(self, ipv4_string):
        assert is_valid_ipv4(ipv4_string) is False

    # D. Cenários Inválidos - Caracteres Não-Dígitos (Viola Regra 2)
    @pytest.mark.parametrize("ipv4_string", [
        "1.2.3.a",             # 13. Letra em octeto
        "1.2.3. 4",            # 14. Espaço em octeto
        " 1.2.3.4",            # 15. Espaço antes do primeiro octeto
        "+1.2.3.4",            # 16. Sinal de mais em octeto
        "-1.2.3.4",            # 17. Sinal de menos em octeto
        "1.2.3.$",             # 18. Outro símbolo em octeto
        "1.2.3.4 ",            # Espaço depois do último octeto
        "1.2.3.4a",            # Letra no final do octeto
        "1.2.3.a4",            # Letra no meio do octeto
    ])
    def test_invalid_ipv4_non_digit_characters(self, ipv4_string):
        assert is_valid_ipv4(ipv4_string) is False

    # E. Cenários Inválidos - Valor do Octeto Fora do Intervalo [0, 255] (Viola Regra 3)
    @pytest.mark.parametrize("ipv4_string", [
        "256.0.0.0",           # 19. Valor imediatamente acima do máximo
        "999.0.0.0",           # 20. Valor muito acima do máximo
        "0.0.0.256",           # 21. Valor imediatamente acima do máximo em outro octeto
        "1.2.3.1000",          # Valor muito acima do máximo em outro octeto
    ])
    def test_invalid_ipv4_octet_out_of_range(self, ipv4_string):
        assert is_valid_ipv4(ipv4_string) is False

    # F. Cenários Inválidos - Zeros à Esquerda (Viola Regra 4)
    @pytest.mark.parametrize("ipv4_string", [
        "01.2.3.4",            # 22. Zero à esquerda em octeto de 2 dígitos
        "00.0.0.0",            # 23. Múltiplos zeros à esquerda
        "007.8.9.10",          # 24. Zero à esquerda em octeto de 3 dígitos
        "0255.0.0.0",          # 25. Zero à esquerda em octeto máximo
        "1.01.2.3",            # Zero à esquerda no segundo octeto
        "1.2.03.4",            # Zero à esquerda no terceiro octeto
        "1.2.3.04",            # Zero à esquerda no quarto octeto
    ])
    def test_invalid_ipv4_leading_zeros(self, ipv4_string):
        assert is_valid_ipv4(ipv4_string) is False

    # G. Cenários de Borda e Invariantes
    @pytest.mark.parametrize("ipv4_string", [
        "",                    # 26. String vazia
        "   ",                 # 27. String com apenas espaços
        "1234567890.1.1.1",    # 28. String com octeto muito longo, mas numérico (viola Regra 3)
    ])
    def test_invalid_ipv4_edge_cases_and_invariants(self, ipv4_string):
        assert is_valid_ipv4(ipv4_string) is False
