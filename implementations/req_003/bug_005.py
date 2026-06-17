# Fault: off-by-one na fronteira adolescente/adulto (<= 18).
# Idade 18 é classificada como "adolescente" em vez de "adulto".
def age_bracket(age: int) -> str:
    if age < 0:
        return "invalido"
    if age <= 11:
        return "crianca"
    if age <= 18:
        return "adolescente"
    if age <= 59:
        return "adulto"
    return "idoso"
