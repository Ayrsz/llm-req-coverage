from solution import triangle_type
import pytest


# Testes para casos de triângulos inválidos devido a lados não positivos (<= 0)
@pytest.mark.parametrize("a, b, c, expected", [
    (0, 1, 1, "invalido"),  # AC6: Um lado é zero
    (1, 0, 1, "invalido"),
    (1, 1, 0, "invalido"),
    (-1, 2, 2, "invalido"), # AC7: Um lado é negativo
    (2, -1, 2, "invalido"),
    (2, 2, -1, "invalido"),
    (0, 0, 1, "invalido"),  # Dois lados são zero
    (0, 1, 0, "invalido"),
    (1, 0, 0, "invalido"),
    (-1, -1, 1, "invalido"), # Dois lados são negativos
    (-1, 1, -1, "invalido"),
    (1, -1, -1, "invalido"),
    (0, 0, 0, "invalido"),  # Todos os lados são zero
    (-1, -1, -1, "invalido"), # Todos os lados são negativos
    (0, -1, 1, "invalido"), # Mistura de zero e negativo
])
def test_invalid_non_positive_sides(a, b, c, expected):
    assert triangle_type(a, b, c) == expected


# Testes para casos de triângulos inválidos devido à violação da desigualdade triangular estrita
@pytest.mark.parametrize("a, b, c, expected", [
    (1, 1, 2, "invalido"),  # AC4: Triângulo degenerado (a + b == c)
    (2, 1, 1, "invalido"),  # Degenerado (simetria)
    (1, 2, 1, "invalido"),  # Degenerado (simetria)
    (3, 4, 7, "invalido"),  # Degenerado
    (7, 3, 4, "invalido"),  # Degenerado (simetria)
    (4, 7, 3, "invalido"),  # Degenerado (simetria)
    (1, 2, 5, "invalido"),  # AC5: Soma de dois lados menor que o terceiro (a + b < c)
    (5, 1, 2, "invalido"),  # Soma menor (simetria)
    (2, 5, 1, "invalido"),  # Soma menor (simetria)
    (1, 1, 3, "invalido"),  # Soma menor
    (10, 2, 3, "invalido"), # Soma menor
    (1, 1, 1000000, "invalido"), # Grande diferença, viola desigualdade
])
def test_invalid_triangle_inequality(a, b, c, expected):
    assert triangle_type(a, b, c) == expected


# Testes para triângulos equiláteros válidos
@pytest.mark.parametrize("a, b, c, expected", [
    (1, 1, 1, "equilatero"),  # Menor triângulo equilátero possível
    (3, 3, 3, "equilatero"),  # AC1: Caso típico
    (100, 100, 100, "equilatero"), # Lados maiores
    (1000000, 1000000, 1000000, "equilatero"), # Lados muito grandes
])
def test_equilateral_triangles(a, b, c, expected):
    assert triangle_type(a, b, c) == expected


# Testes para triângulos isósceles válidos
@pytest.mark.parametrize("a, b, c, expected", [
    (5, 5, 8, "isosceles"),  # AC2: Dois lados iguais (a == b)
    (8, 5, 5, "isosceles"),  # AC8: Dois lados iguais (b == c, simetria)
    (5, 8, 5, "isosceles"),  # Dois lados iguais (a == c, simetria)
    (2, 2, 1, "isosceles"),  # Pequeno
    (10, 10, 1, "isosceles"), # Dois lados grandes, um pequeno
    (1, 10, 10, "isosceles"), # Um lado pequeno, dois grandes
    (100, 100, 150, "isosceles"),
    (1000000, 1000000, 1, "isosceles"), # Lados muito grandes, um pequeno
    (1, 1000000, 1000000, "isosceles"),
])
def test_isosceles_triangles(a, b, c, expected):
    assert triangle_type(a, b, c) == expected


# Testes para triângulos escalenos válidos
@pytest.mark.parametrize("a, b, c, expected", [
    (2, 3, 4, "escaleno"),  # AC3: Caso típico, menor escaleno válido
    (3, 4, 5, "escaleno"),  # Triângulo retângulo
    (4, 3, 2, "escaleno"),  # Simetria
    (5, 3, 4, "escaleno"),  # Simetria
    (7, 8, 9, "escaleno"),
    (10, 11, 12, "escaleno"),
    (100, 101, 102, "escaleno"),
    (1000000, 1000001, 1000002, "escaleno"), # Lados muito grandes
])
def test_scalene_triangles(a, b, c, expected):
    assert triangle_type(a, b, c) == expected
