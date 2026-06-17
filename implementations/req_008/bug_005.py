# Fault: guarda ausente (remove o tratamento de year <= 0 inválido).
# Faz year=0 retornar True (0 % 400 == 0) em vez de False.
def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
