def is_leap_year(year: int) -> bool:
    # Ano não positivo é entrada inválida: não é bissexto.
    if year <= 0:
        return False
    # Regra gregoriana: divisível por 4 e (não por 100 ou por 400).
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
