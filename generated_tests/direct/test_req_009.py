from solution import days_between
import pytest

# Testes para casos típicos e de borda (valores-limite)

@pytest.mark.parametrize(
    "start_date, end_date, expected_diff",
    [
        # AC1: Mesma data
        ("2021-01-01", "2021-01-01", 0),
        # AC2: Diferença positiva de um dia
        ("2021-01-01", "2021-01-02", 1),
        # AC3: Diferença negativa de um dia
        ("2021-01-02", "2021-01-01", -1),
        # Diferença positiva maior
        ("2021-01-01", "2021-01-31", 30),
        # Diferença negativa maior
        ("2021-01-31", "2021-01-01", -30),
        # Diferença entre meses
        ("2021-01-15", "2021-02-15", 31),
        ("2021-02-15", "2021-01-15", -31),
        # Diferença entre anos
        ("2021-01-01", "2022-01-01", 365),
        ("2022-01-01", "2021-01-01", -365),
    ],
)
def test_days_between_typical_cases(start_date, end_date, expected_diff):
    """
    Verifica casos típicos de diferença de dias: zero, positivo e negativo.
    """
    assert days_between(start_date, end_date) == expected_diff


@pytest.mark.parametrize(
    "start_date, end_date, expected_diff",
    [
        # AC4: Atravessa 29/02 bissexto
        ("2020-02-28", "2020-03-01", 2),
        # Ano bissexto: 29/02 existe
        ("2020-02-27", "2020-02-29", 2),
        ("2020-02-29", "2020-03-01", 1),
        ("2020-03-01", "2020-02-29", -1),
        # Ano não bissexto: 29/02 não existe
        ("2019-02-28", "2019-03-01", 1),
        # AC5: Ano completo não bissexto
        ("2019-01-01", "2020-01-01", 365),
        # Ano completo bissexto
        ("2020-01-01", "2021-01-01", 366),
        # Ano completo bissexto (inverso)
        ("2021-01-01", "2020-01-01", -366),
        # Múltiplos anos, incluindo bissextos
        ("2019-01-01", "2021-01-01", 731),  # 365 (2019) + 366 (2020) = 731
        ("2021-01-01", "2019-01-01", -731),
    ],
)
def test_days_between_leap_year_and_year_boundaries(start_date, end_date, expected_diff):
    """
    Verifica o comportamento em anos bissextos e limites de ano.
    """
    assert days_between(start_date, end_date) == expected_diff


# Testes para entradas inválidas (formato ou data inexistente)

@pytest.mark.parametrize(
    "start_date, end_date, expected_sentinel",
    [
        # AC6: Data inexistente no argumento start
        ("2021-02-30", "2021-01-01", -999999),
        # Data inexistente no argumento end
        ("2021-01-01", "2021-02-30", -999999),
        # Mês inválido
        ("2021-13-01", "2021-01-01", -999999),
        ("2021-01-01", "2021-13-01", -999999),
        # Dia inválido
        ("2021-01-32", "2021-01-01", -999999),
        ("2021-01-01", "2021-01-32", -999999),
        # Ambos inválidos
        ("2021-02-30", "2021-13-01", -999999),
    ],
)
def test_days_between_invalid_date_non_existent(start_date, end_date, expected_sentinel):
    """
    Verifica o retorno do sentinela para datas que não existem.
    """
    assert days_between(start_date, end_date) == expected_sentinel


@pytest.mark.parametrize(
    "start_date, end_date, expected_sentinel",
    [
        # AC7: Formato inválido no argumento start
        ("01/01/2021", "2021-01-01", -999999),
        # Formato inválido no argumento end
        ("2021-01-01", "01/01/2021", -999999),
        # Formato com mês/dia de um dígito
        ("2021-1-1", "2021-01-01", -999999),
        ("2021-01-01", "2021-1-1", -999999),
        # String vazia
        ("", "2021-01-01", -999999),
        ("2021-01-01", "", -999999),
        # String malformada
        ("not-a-date", "2021-01-01", -999999),
        ("2021-01-01", "not-a-date", -999999),
        # Formato com ano de 2 dígitos
        ("21-01-01", "2021-01-01", -999999),
        ("2021-01-01", "21-01-01", -999999),
        # Formato com separador diferente
        ("2021.01.01", "2021-01-01", -999999),
        ("2021-01-01", "2021.01.01", -999999),
        # Ambos com formato inválido
        ("01/01/2021", "not-a-date", -999999),
    ],
)
def test_days_between_invalid_date_format(start_date, end_date, expected_sentinel):
    """
    Verifica o retorno do sentinela para datas com formato inválido.
    """
    assert days_between(start_date, end_date) == expected_sentinel


# Testes para invariantes

@pytest.mark.parametrize(
    "date_a, date_b",
    [
        ("2021-01-01", "2021-01-05"),
        ("2020-02-28", "2020-03-01"),
        ("1999-12-31", "2000-01-01"),
        ("2023-07-15", "2023-07-15"),
    ],
)
def test_days_between_invariants_symmetry(date_a, date_b):
    """
    Verifica a invariante: days_between(a, b) == -days_between(b, a).
    """
    if days_between(date_a, date_b) != -999999 and days_between(date_b, date_a) != -999999:
        assert days_between(date_a, date_b) == -days_between(date_b, date_a)
    else:
        # Se uma das datas for inválida, ambas devem retornar o sentinela
        assert days_between(date_a, date_b) == -999999
        assert days_between(date_b, date_a) == -999999


@pytest.mark.parametrize(
    "date_str",
    [
        "2021-01-01",
        "2020-02-29",
        "1900-01-01",
        "2099-12-31",
    ],
)
def test_days_between_invariants_same_date_is_zero(date_str):
    """
    Verifica a invariante: days_between(a, a) == 0 para 'a' válido.
    """
    assert days_between(date_str, date_str) == 0


def test_days_between_return_type_is_int():
    """
    Verifica que o tipo de retorno é sempre int.
    """
    assert isinstance(days_between("2021-01-01", "2021-01-02"), int)
    assert isinstance(days_between("2021-01-01", "2021-01-01"), int)
    assert isinstance(days_between("2021-01-02", "2021-01-01"), int)
    assert isinstance(days_between("invalid-date", "2021-01-01"), int)
