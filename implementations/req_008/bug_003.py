# Fault: ramo/retorno trocado (negação do resultado da regra).
# Inverte todos os veredictos válidos: bissexto vira não-bissexto e vice-versa.
def is_leap_year(year: int) -> bool:
    if year <= 0:
        return False
    return not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
