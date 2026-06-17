def triangle_type(a: int, b: int, c: int) -> str:
    # Guarda: lados positivos e desigualdade triangular estrita.
    if a <= 0 or b <= 0 or c <= 0:
        return "invalido"
    if a + b <= c or a + c <= b or b + c <= a:
        return "invalido"
    # Classificação por igualdade de lados.
    if a == b == c:
        return "equilatero"
    if a == b or a == c or b == c:
        return "isosceles"
    return "escaleno"
