# Fault: constante/literal errado (400 -> 200) na exceção secular.
# Faz 2000 deixar de ser bissexto (2000 % 200 == 0, mas a regra usa 400).
def is_leap_year(year: int) -> bool:
    if year <= 0:
        return False
    return year % 4 == 0 and (year % 100 != 0 or year % 200 == 0)
