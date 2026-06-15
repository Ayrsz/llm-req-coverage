# Fault: off-by-one na fronteira adulto/idoso (<= 60).
# Idade 60 é classificada como "adulto" em vez de "idoso".
def age_bracket(age: int) -> str:
    if age < 0:
        return "invalido"
    if age <= 11:
        return "crianca"
    if age <= 17:
        return "adolescente"
    if age <= 60:
        return "adulto"
    return "idoso"
