import pytest
from solution import is_leap_year


@pytest.mark.parametrize(
    "year, expected",
    [
        # Casos inválidos (year <= 0)
        (0, False),  # Valor-limite inválido (AC6)
        (-1, False),
        (-4, False),  # Exemplo de AC6
        (-100, False),
        (-2000, False),
    ],
)
def test_is_leap_year_invalid_input(year, expected):
    """Testa anos inválidos (zero ou negativos)."""
    assert is_leap_year(year) is expected


@pytest.mark.parametrize(
    "year, expected",
    [
        # Casos de anos bissextos (divisíveis por 400)
        (2000, True),  # AC1, Valor-limite
        (1600, True),
        (2400, True),
        (400, True),
        (800, True),
    ],
)
def test_is_leap_year_divisible_by_400(year, expected):
    """Testa anos bissextos divisíveis por 400."""
    assert is_leap_year(year) is expected


@pytest.mark.parametrize(
    "year, expected",
    [
        # Casos de anos não bissextos (divisíveis por 100, mas não por 400)
        (1900, False),  # AC2, Valor-limite
        (2100, False),  # AC4, Valor-limite
        (1800, False),
        (1700, False),
        (100, False),
        (300, False),
    ],
)
def test_is_leap_year_divisible_by_100_not_400(year, expected):
    """Testa anos não bissextos divisíveis por 100, mas não por 400."""
    assert is_leap_year(year) is expected


@pytest.mark.parametrize(
    "year, expected",
    [
        # Casos de anos bissextos (divisíveis por 4, mas não por 100)
        (2004, True),  # AC3, Valor-limite
        (4, True),  # Menor positivo divisível por 4 (Valor-limite)
        (8, True),
        (12, True),
        (1996, True),
        (2008, True),
    ],
)
def test_is_leap_year_divisible_by_4_not_100(year, expected):
    """Testa anos bissextos divisíveis por 4, mas não por 100."""
    assert is_leap_year(year) is expected


@pytest.mark.parametrize(
    "year, expected",
    [
        # Casos de anos não bissextos (não divisíveis por 4)
        (2001, False),  # AC5
        (1, False),  # Valor-limite (não divisível por 4)
        (2, False),
        (3, False),
        (5, False),
        (1999, False),
        (2002, False),
        (2003, False),
    ],
)
def test_is_leap_year_not_divisible_by_4(year, expected):
    """Testa anos não bissextos (não divisíveis por 4)."""
    assert is_leap_year(year) is expected
