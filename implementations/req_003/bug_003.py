# Fault: caso ausente (não trata idade negativa como inválida).
# Idade negativa cai em "crianca".
def age_bracket(age: int) -> str:
    if age <= 11:
        return "crianca"
    if age <= 17:
        return "adolescente"
    if age <= 59:
        return "adulto"
    return "idoso"
