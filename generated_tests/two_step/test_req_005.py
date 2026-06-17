import pytest
from solution import triangle_type

class TestTriangleType:
    # Cenários de Teste para `triangle_type(a, b, c)`

    # 1. Técnica: Análise de Valores-Limite / Caso Negativo (lado zero)
    def test_invalid_side_zero_one_side(self):
        assert triangle_type(0, 1, 1) == "invalido"

    # 2. Técnica: Análise de Valores-Limite / Caso Negativo (lado negativo)
    def test_invalid_side_negative_one_side(self):
        assert triangle_type(-1, 2, 2) == "invalido"

    # 3. Técnica: Particionamento por Equivalência / Caso Negativo (dois lados zero)
    def test_invalid_side_zero_two_sides(self):
        assert triangle_type(0, 0, 5) == "invalido"

    # 4. Técnica: Particionamento por Equivalência / Caso Negativo (dois lados negativos)
    def test_invalid_side_negative_two_sides(self):
        assert triangle_type(-2, -3, 5) == "invalido"

    # 5. Técnica: Particionamento por Equivalência / Caso Negativo (todos os lados zero)
    def test_invalid_side_zero_all_sides(self):
        assert triangle_type(0, 0, 0) == "invalido"

    # 6. Técnica: Particionamento por Equivalência / Caso Negativo (todos os lados negativos)
    def test_invalid_side_negative_all_sides(self):
        assert triangle_type(-1, -1, -1) == "invalido"

    # 7. Técnica: Particionamento por Equivalência / Caso Negativo (combinação de lado zero e negativo)
    def test_invalid_side_zero_and_negative(self):
        assert triangle_type(0, -1, 5) == "invalido"

    # 8. Técnica: Análise de Valores-Limite / Caso Negativo (triângulo degenerado: `a + b == c`)
    def test_invalid_degenerate_sum_equals_c(self):
        assert triangle_type(1, 1, 2) == "invalido"

    # 9. Técnica: Análise de Valores-Limite / Caso Negativo (triângulo degenerado: `a + c == b`)
    def test_invalid_degenerate_sum_equals_b(self):
        assert triangle_type(1, 2, 1) == "invalido"

    # 10. Técnica: Análise de Valores-Limite / Caso Negativo (triângulo degenerado: `b + c == a`)
    def test_invalid_degenerate_sum_equals_a(self):
        assert triangle_type(2, 1, 1) == "invalido"

    # 11. Técnica: Análise de Valores-Limite / Caso Negativo (triângulo degenerado com lados maiores)
    def test_invalid_degenerate_larger_sides(self):
        assert triangle_type(5, 5, 10) == "invalido"

    # 12. Técnica: Particionamento por Equivalência / Caso Negativo (triângulo impossível: `a + b < c`)
    def test_invalid_impossible_sum_less_than_c(self):
        assert triangle_type(1, 2, 5) == "invalido"

    # 13. Técnica: Particionamento por Equivalência / Caso Negativo (triângulo impossível: `a + c < b`)
    def test_invalid_impossible_sum_less_than_b(self):
        assert triangle_type(1, 5, 2) == "invalido"

    # 14. Técnica: Particionamento por Equivalência / Caso Negativo (triângulo impossível: `b + c < a`)
    def test_invalid_impossible_sum_less_than_a(self):
        assert triangle_type(5, 1, 2) == "invalido"

    # 15. Técnica: Particionamento por Equivalência / Caso Negativo (triângulo impossível com grande diferença)
    def test_invalid_impossible_large_difference(self):
        assert triangle_type(1, 1, 100) == "invalido"

    # 16. Técnica: Análise de Valores-Limite / Caso de Borda (menor triângulo equilátero válido)
    def test_equilateral_smallest(self):
        assert triangle_type(1, 1, 1) == "equilatero"

    # 17. Técnica: Particionamento por Equivalência (triângulo equilátero típico)
    def test_equilateral_typical(self):
        assert triangle_type(3, 3, 3) == "equilatero"

    # 18. Técnica: Particionamento por Equivalência (triângulo equilátero com lados maiores)
    def test_equilateral_larger_sides(self):
        assert triangle_type(10, 10, 10) == "equilatero"

    # 19. Técnica: Particionamento por Equivalência (triângulo isósceles: `a = b`)
    def test_isosceles_a_equals_b(self):
        assert triangle_type(5, 5, 8) == "isosceles"

    # 20. Técnica: Particionamento por Equivalência / Invariante (triângulo isósceles: `a = c`, simetria)
    def test_isosceles_a_equals_c_symmetry(self):
        assert triangle_type(5, 8, 5) == "isosceles"

    # 21. Técnica: Particionamento por Equivalência / Invariante (triângulo isósceles: `b = c`, simetria)
    def test_isosceles_b_equals_c_symmetry(self):
        assert triangle_type(8, 5, 5) == "isosceles"

    # 22. Técnica: Análise de Valores-Limite (triângulo isósceles: lado diferente é o menor possível)
    def test_isosceles_different_side_smallest(self):
        assert triangle_type(2, 2, 1) == "isosceles"

    # 23. Técnica: Análise de Valores-Limite (triângulo isósceles: lado diferente é o maior possível sem ser degenerado)
    def test_isosceles_different_side_largest_near_degenerate(self):
        assert triangle_type(5, 5, 9) == "isosceles"

    # 24. Técnica: Análise de Valores-Limite (triângulo isósceles: lados iguais são os menores possíveis)
    def test_isosceles_equal_sides_smallest(self):
        assert triangle_type(1, 2, 2) == "isosceles"

    # 25. Técnica: Análise de Valores-Limite (triângulo escaleno: válido por pouco)
    def test_scalene_valid_by_little(self):
        assert triangle_type(2, 3, 4) == "escaleno"

    # 26. Técnica: Particionamento por Equivalência (triângulo escaleno típico)
    def test_scalene_typical_pythagorean(self):
        assert triangle_type(3, 4, 5) == "escaleno"

    # 27. Técnica: Análise de Valores-Limite (triângulo escaleno: lados próximos ao limite de degeneração)
    def test_scalene_sides_near_degenerate_limit(self):
        assert triangle_type(3, 4, 6) == "escaleno"

    # 28. Técnica: Particionamento por Equivalência (triângulo escaleno com lados maiores)
    def test_scalene_larger_sides(self):
        assert triangle_type(7, 8, 9) == "escaleno"

    # 29. Técnica: Invariante (Simetria: permutação de lados para um escaleno)
    def test_scalene_symmetry_permutation(self):
        assert triangle_type(4, 2, 3) == "escaleno"
