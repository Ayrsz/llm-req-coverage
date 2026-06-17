# Fault: fronteira/off-by-one na guarda de validade (< em vez de <=).
# Ano 0 passa a ser avaliado pela regra (0 % 400 == 0 -> True) em vez de False.
def is_leap_year(year: int) -> bool:
    if year < 0:
        return False
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
