import pytest
from solution import days_between

# Cenários de Teste para days_between(start: str, end: str) -> int

# 1. Técnica: Classe de Equivalência (mesma data), Análise de Valores-Limite (fronteira zero)
#    Entrada: start="2021-01-01", end="2021-01-01"
#    Resultado Esperado: 0
#    (Cobre AC1)
def test_days_between_same_date():
    assert days_between("2021-01-01", "2021-01-01") == 0

# 2. Técnica: Classe de Equivalência (end > start), Análise de Valores-Limite (fronteira +1)
#    Entrada: start="2021-01-01", end="2021-01-02"
#    Resultado Esperado: 1
#    (Cobre AC2)
def test_days_between_one_day_positive():
    assert days_between("2021-01-01", "2021-01-02") == 1

# 3. Técnica: Classe de Equivalência (end < start), Análise de Valores-Limite (fronteira -1)
#    Entrada: start="2021-01-02", end="2021-01-01"
#    Resultado Esperado: -1
#    (Cobre AC3)
def test_days_between_one_day_negative():
    assert days_between("2021-01-02", "2021-01-01") == -1

# 4. Técnica: Classe de Equivalência (end > start, diferença média)
#    Entrada: start="2021-01-15", end="2021-04-20"
#    Resultado Esperado: 95
def test_days_between_medium_positive_diff():
    assert days_between("2021-01-15", "2021-04-20") == 95

# 5. Técnica: Classe de Equivalência (end < start, diferença média)
#    Entrada: start="2021-04-20", end="2021-01-15"
#    Resultado Esperado: -95
def test_days_between_medium_negative_diff():
    assert days_between("2021-04-20", "2021-01-15") == -95

# 6. Técnica: Análise de Valores-Limite (ano bissexto, atravessando 29/02)
#    Entrada: start="2020-02-28", end="2020-03-01"
#    Resultado Esperado: 2
#    (Cobre AC4)
def test_days_between_leap_year_crossing_feb29():
    assert days_between("2020-02-28", "2020-03-01") == 2

# 7. Técnica: Análise de Valores-Limite (ano não bissexto, atravessando 28/02)
#    Entrada: start="2019-02-28", end="2019-03-01"
#    Resultado Esperado: 1
def test_days_between_non_leap_year_crossing_feb28():
    assert days_between("2019-02-28", "2019-03-01") == 1

# 8. Técnica: Análise de Valores-Limite (ano completo não bissexto)
#    Entrada: start="2019-01-01", end="2020-01-01"
#    Resultado Esperado: 365
#    (Cobre AC5)
def test_days_between_full_non_leap_year():
    assert days_between("2019-01-01", "2020-01-01") == 365

# 9. Técnica: Análise de Valores-Limite (ano completo bissexto)
#    Entrada: start="2020-01-01", end="2021-01-01"
#    Resultado Esperado: 366
def test_days_between_full_leap_year():
    assert days_between("2020-01-01", "2021-01-01") == 366

# 10. Técnica: Análise de Valores-Limite (data de início em 29/02 de ano bissexto)
#     Entrada: start="2020-02-29", end="2020-03-01"
#     Resultado Esperado: 1
def test_days_between_start_on_feb29():
    assert days_between("2020-02-29", "2020-03-01") == 1

# 11. Técnica: Análise de Valores-Limite (data de fim em 29/02 de ano bissexto)
#     Entrada: start="2020-02-28", end="2020-02-29"
#     Resultado Esperado: 1
def test_days_between_end_on_feb29():
    assert days_between("2020-02-28", "2020-02-29") == 1

# 12. Técnica: Análise de Valores-Limite (diferença entre último dia de um mês e primeiro dia do próximo)
#     Entrada: start="2021-01-31", end="2021-02-01"
#     Resultado Esperado: 1
def test_days_between_month_transition():
    assert days_between("2021-01-31", "2021-02-01") == 1

# 13. Técnica: Análise de Valores-Limite (diferença entre último dia de um ano e primeiro dia do próximo)
#     Entrada: start="2021-12-31", end="2022-01-01"
#     Resultado Esperado: 1
def test_days_between_year_transition():
    assert days_between("2021-12-31", "2022-01-01") == 1

# 14-22. Casos Negativos (datas inválidas ou formatos incorretos)
# Agrupados usando parametrização para cobrir AC6 e AC7 e outros casos de erro.
@pytest.mark.parametrize(
    "start_date, end_date, expected",
    [
        # 14. Data inexistente no argumento start (Cobre AC6)
        ("2021-02-30", "2021-01-01", -999999),
        # 15. Formato inválido no argumento start (Cobre AC7)
        ("01/01/2021", "2021-01-01", -999999),
        # 16. Data inexistente no argumento end
        ("2021-01-01", "2021-02-30", -999999),
        # 17. Formato inválido no argumento end
        ("2021-01-01", "01/01/2021", -999999),
        # 18. Ambos argumentos com formato inválido
        ("invalid-date", "another-invalid", -999999),
        # 19. Ambos argumentos com data inexistente
        ("2021-02-30", "2021-13-01", -999999),
        # 20. String vazia para start
        ("", "2021-01-01", -999999),
        # 21. Mês inválido (ex: "00")
        ("2021-00-01", "2021-01-01", -999999),
        # 22. Dia inválido (ex: "00")
        ("2021-01-00", "2021-01-01", -999999),
        # Outros formatos inválidos
        ("2021-1-1", "2021-01-01", -999999),
        ("2021/01/01", "2021-01-01", -999999),
        ("2021-01-01 ", "2021-01-01", -999999), # Espaço no final
        (" 2021-01-01", "2021-01-01", -999999), # Espaço no início
        ("2021-01-01T00:00:00", "2021-01-01", -999999), # Formato datetime
    ],
)
def test_days_between_invalid_inputs(start_date, end_date, expected):
    assert days_between(start_date, end_date) == expected

# 23. Técnica: Casos de Borda (diferença entre data mínima e máxima suportada)
#     Entrada: start="0001-01-01", end="9999-12-31"
#     Resultado Esperado: 3652424
def test_days_between_min_max_dates():
    assert days_between("0001-01-01", "9999-12-31") == 3652424

# 24. Técnica: Casos de Borda (diferença entre data máxima e mínima suportada, negativo)
#     Entrada: start="9999-12-31", end="0001-01-01"
#     Resultado Esperado: -3652424
def test_days_between_max_min_dates():
    assert days_between("9999-12-31", "0001-01-01") == -3652424

# 25. Técnica: Casos de Borda (atravessando múltiplos anos bissextos)
#     Entrada: start="2019-01-01", end="2025-01-01"
#     Resultado Esperado: 2192 (2020 e 2024 são bissextos)
def test_days_between_multiple_leap_years():
    assert days_between("2019-01-01", "2025-01-01") == 2192

# 26. Técnica: Casos de Borda (atravessando virada de século não bissexto)
#     Entrada: start="1899-12-31", end="1900-01-01"
#     Resultado Esperado: 1 (1900 não foi bissexto)
def test_days_between_century_transition_non_leap():
    assert days_between("1899-12-31", "1900-01-01") == 1

# 27. Técnica: Casos de Borda (atravessando virada de milênio bissexto, cobrindo 29/02)
#     Entrada: start="1999-03-01", end="2000-03-01"
#     Resultado Esperado: 366 (2000 foi bissexto)
def test_days_between_millennium_transition_leap():
    assert days_between("1999-03-01", "2000-03-01") == 366

# 28. Técnica: Invariante (days_between(a, b) == -days_between(b, a))
#     Entrada: a="2021-01-01", b="2021-01-05"
#     Resultado Esperado: days_between(a, b) deve ser 5 e days_between(b, a) deve ser -5.
#     A asserção é days_between(a, b) == -days_between(b, a).
def test_days_between_invariant_symmetry():
    date_a = "2021-01-01"
    date_b = "2021-01-05"
    result_ab = days_between(date_a, date_b)
    result_ba = days_between(date_b, date_a)
    assert result_ab == 4
    assert result_ba == -4
    assert result_ab == -result_ba

# Teste adicional para o invariante days_between(a, a) == 0
def test_days_between_invariant_same_date_is_zero():
    date_a = "2023-07-15"
    assert days_between(date_a, date_a) == 0
