# Fault: guarda ausente (falta um dos três ramos da desigualdade triangular).
# Sem checar "b + c <= a", um triângulo inválido com 'a' grande escapa a
# validação e é classificado como se fosse válido.
def triangle_type(a: int, b: int, c: int) -> str:
    if a <= 0 or b <= 0 or c <= 0:
        return "invalido"
    if a + b <= c or a + c <= b:
        return "invalido"
    if a == b == c:
        return "equilatero"
    if a == b or a == c or b == c:
        return "isosceles"
    return "escaleno"
