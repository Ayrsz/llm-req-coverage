# Fault: operador errado (or em vez de and no teste de equilátero).
# Dois lados iguais já satisfazem a condição e viram "equilatero".
def triangle_type(a: int, b: int, c: int) -> str:
    if a <= 0 or b <= 0 or c <= 0:
        return "invalido"
    if a + b <= c or a + c <= b or b + c <= a:
        return "invalido"
    if a == b or b == c:
        return "equilatero"
    if a == b or a == c or b == c:
        return "isosceles"
    return "escaleno"
