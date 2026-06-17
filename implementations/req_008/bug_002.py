# Fault: operador errado (and -> or) na composição da regra gregoriana.
# Faz 1900 ser classificado como bissexto (4 | 1900 OR ...).
def is_leap_year(year: int) -> bool:
    if year <= 0:
        return False
    return year % 4 == 0 or (year % 100 != 0 or year % 400 == 0)
