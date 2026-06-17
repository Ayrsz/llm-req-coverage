# Fault: rótulo de saída errado (retorna "velho" em vez de "idoso").
def age_bracket(age: int) -> str:
    if age < 0:
        return "invalido"
    if age <= 11:
        return "crianca"
    if age <= 17:
        return "adolescente"
    if age <= 59:
        return "adulto"
    return "velho"
