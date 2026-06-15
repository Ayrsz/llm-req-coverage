# Fault: off-by-one na fronteira criança/adolescente (<= 12).
# Idade 12 é classificada como "crianca" em vez de "adolescente".
def age_bracket(age: int) -> str:
    if age < 0:
        return "invalido"
    if age <= 12:
        return "crianca"
    if age <= 17:
        return "adolescente"
    if age <= 59:
        return "adulto"
    return "idoso"
