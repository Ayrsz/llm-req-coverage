import pytest
from solution import is_leap_year


@pytest.mark.parametrize("year, expected", [
    # Cenários de Classes de Equivalência (Equivalence Partitioning)
    # Classe: Ano divisível por 400 (Bissexto)
    (2000, True),  # Cobre AC1
    (2400, True),

    # Classe: Ano divisível por 100, mas não por 400 (Não Bissexto)
    (1900, False), # Cobre AC2
    (2100, False), # Cobre AC4

    # Classe: Ano divisível por 4, mas não por 100 (Bissexto)
    (2004, True),  # Cobre AC3
    (2008, True),

    # Classe: Ano não divisível por 4 (Não Bissexto)
    (2001, False), # Cobre AC5
    (2002, False),

    # Classe: Ano não positivo (`year <= 0`) (Inválido, Não Bissexto)
    (-100, False),
    (-400, False),

    # Cenários de Análise de Valores-Limite (Boundary Value Analysis)
    # Limite do domínio válido (`year >= 1`)
    (1, False), # menor ano positivo
    (2, False), # vizinho de 1

    # Limite do domínio inválido (`year <= 0`)
    (0, False), # limite superior do inválido (Cobre parte de AC6)
    (-1, False), # vizinho de 0, negativo

    # Limites em torno da divisibilidade por 4
    (3, False), # antes de um múltiplo de 4
    (4, True),  # primeiro múltiplo de 4, não 100
    (5, False), # depois de um múltiplo de 4

    # Limites em torno da divisibilidade por 100 (não 400)
    (99, False),   # antes de 100
    (100, False),  # múltiplo de 100, não 400
    (101, False),  # depois de 100
    (1899, False), # antes de 1900
    (1901, False), # depois de 1900

    # Limites em torno da divisibilidade por 400
    (399, False), # antes de 400
    (400, True),  # múltiplo de 400
    (401, False), # depois de 400
    (1999, False), # antes de 2000
    # (2000, True), # já coberto acima
    # (2001, False), # já coberto acima

    # Cenários de Casos Negativos / Entradas Inválidas
    # (0, False), # já coberto acima
    (-4, False), # Entrada negativa (múltiplo de 4) (Cobre parte de AC6)
    (-5, False), # Entrada negativa (não múltiplo de 4)

    # Cenários de Casos de Borda e Invariantes
    # (4, True), # Menor ano positivo bissexto (já coberto acima)
    (10000, True), # Ano grande, divisível por 400
    (9900, False), # Ano grande, divisível por 100 mas não por 400
    (9904, True),  # Ano grande, divisível por 4 mas não por 100
    (9999, False), # Ano grande, não divisível por 4
])
def test_is_leap_year_cases(year: int, expected: bool):
    """
    Testa a função is_leap_year com uma variedade de anos, cobrindo
    classes de equivalência, valores-limite e entradas inválidas.
    """
    result = is_leap_year(year)
    assert result is expected, f"Para o ano {year}, esperado {expected}, mas obteve {result}"


@pytest.mark.parametrize("year", [
    2000,  # Bissexto
    1900,  # Não bissexto
    2001,  # Não bissexto
    0,     # Inválido
    -100   # Inválido
])
def test_is_leap_year_returns_boolean_type(year: int):
    """
    Verifica o invariante de que a função sempre retorna um tipo booleano.
    """
    result = is_leap_year(year)
    assert isinstance(result, bool), f"Para o ano {year}, o tipo de retorno deveria ser bool, mas foi {type(result)}"
