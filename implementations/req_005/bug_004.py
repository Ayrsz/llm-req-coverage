# Fault: constante/literal errado (compara lado com 1 em vez de 0).
# Lados iguais a 1 passam a ser tratados como inválidos.
def triangle_type(a: int, b: int, c: int) -> str:
    if a <= 1 or b <= 1 or c <= 1:
        return "invalido"
    if a + b <= c or a + c <= b or b + c <= a:
        return "invalido"
    if a == b == c:
        return "equilatero"
    if a == b or a == c or b == c:
        return "isosceles"
    return "escaleno"
