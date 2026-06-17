# Fault: off-by-one na desigualdade triangular (< em vez de <=).
# Triângulo degenerado (a + b == c) passa a ser aceito como válido.
def triangle_type(a: int, b: int, c: int) -> str:
    if a <= 0 or b <= 0 or c <= 0:
        return "invalido"
    if a + b < c or a + c < b or b + c < a:
        return "invalido"
    if a == b == c:
        return "equilatero"
    if a == b or a == c or b == c:
        return "isosceles"
    return "escaleno"
