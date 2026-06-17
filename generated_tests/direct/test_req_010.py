import pytest
from solution import average_above


def test_empty_list_returns_zero():
    """
    AC3: average_above([], 5) == 0.0 (lista vazia).
    """
    assert average_above([], 5) == pytest.approx(0.0)


def test_no_elements_above_threshold_all_below():
    """
    Testa quando todos os elementos estão abaixo do limiar.
    """
    assert average_above([1, 2, 3], 5) == pytest.approx(0.0)


def test_no_elements_above_threshold_all_equal():
    """
    AC4: average_above([5, 5, 5], 5) == 0.0 (nenhum estritamente maior).
    """
    assert average_above([5, 5, 5], 5) == pytest.approx(0.0)


def test_no_elements_above_threshold_mixed_below_and_equal():
    """
    Testa quando há elementos abaixo e iguais ao limiar, mas nenhum acima.
    """
    assert average_above([1, 5, 3, 5, 2], 5) == pytest.approx(0.0)


def test_no_elements_above_threshold_with_negative_values_and_positive_threshold():
    """
    Testa com valores negativos e limiar positivo, onde nenhum qualifica.
    """
    assert average_above([-1, -5, -10], 0) == pytest.approx(0.0)


def test_some_elements_above_threshold_integers():
    """
    AC1: average_above([1, 2, 3, 4], 2) == 3.5 (média de 3 e 4).
    """
    assert average_above([1, 2, 3, 4], 2) == pytest.approx(3.5)


def test_some_elements_above_threshold_floats():
    """
    Testa com valores de ponto flutuante e alguns qualificando.
    (2.5 + 3.5 + 4.0) / 3 = 10.0 / 3 = 3.333... -> 3.33
    """
    assert average_above([1.0, 2.5, 3.5, 4.0], 2.0) == pytest.approx(3.33)


def test_some_elements_above_threshold_mixed_types():
    """
    Testa com lista contendo inteiros e floats.
    Qualificados: 2.5, 3, 4.5. Soma = 10.0. Média = 10.0 / 3 = 3.333... -> 3.33
    """
    assert average_above([1, 2.5, 3, 4.5], 2) == pytest.approx(3.33)


def test_some_elements_above_threshold_with_negative_values_and_negative_threshold():
    """
    Testa com valores negativos e limiar negativo.
    Qualificados: -1, 0, 5. Soma = 4. Média = 4 / 3 = 1.333... -> 1.33
    """
    assert average_above([-10, -5, -1, 0, 5], -3) == pytest.approx(1.33)


def test_some_elements_above_threshold_with_zero_threshold():
    """
    Testa com limiar zero.
    Qualificados: 1, 2. Soma = 3. Média = 3 / 2 = 1.5
    """
    assert average_above([-5, 0, 1, 2], 0) == pytest.approx(1.5)


def test_all_elements_above_threshold_integers():
    """
    Testa quando todos os elementos são maiores que o limiar.
    """
    assert average_above([10, 20, 30], 5) == pytest.approx(20.0)


def test_all_elements_above_threshold_floats():
    """
    Testa com todos os elementos floats acima do limiar.
    (10.1 + 20.2 + 30.3) / 3 = 60.6 / 3 = 20.2
    """
    assert average_above([10.1, 20.2, 30.3], 5.0) == pytest.approx(20.2)


def test_all_elements_above_threshold_with_negative_values_and_negative_threshold():
    """
    Testa com todos os elementos negativos acima de um limiar negativo.
    Soma = -1 -0.5 + 0 + 0.5 + 1 = 0.0. Média = 0.0
    """
    assert average_above([-1, -0.5, 0.0, 0.5, 1.0], -2) == pytest.approx(0.0)


def test_single_element_equal_to_threshold():
    """
    AC2: average_above([10], 10) == 0.0 (igual ao limiar é descartado).
    """
    assert average_above([10], 10) == pytest.approx(0.0)


def test_single_element_just_above_threshold():
    """
    Valores-limite: average_above([10.0001], 10) -> 10.0.
    """
    assert average_above([10.0001], 10) == pytest.approx(10.0)


def test_single_element_above_threshold():
    """
    Testa com um único elemento que qualifica.
    """
    assert average_above([15], 10) == pytest.approx(15.0)


def test_threshold_is_large_positive_number():
    """
    Testa com um limiar positivo grande.
    """
    assert average_above([1, 100, 1000], 500) == pytest.approx(1000.0)


def test_threshold_is_large_negative_number():
    """
    Testa com um limiar negativo grande.
    Qualificados: -1000, -500, -100. Soma = -1600. Média = -1600 / 3 = -533.333... -> -533.33
    """
    assert average_above([-1000, -500, -100], -10000) == pytest.approx(-533.33)


def test_rounding_acceptance_criteria_5():
    """
    AC5: average_above([1.111, 2.222, 3.333], 0) == 2.22 (arredondamento para 2 casas).
    (1.111 + 2.222 + 3.333) / 3 = 6.666 / 3 = 2.222 -> 2.22
    """
    assert average_above([1.111, 2.222, 3.333], 0) == pytest.approx(2.22)


@pytest.mark.parametrize("values, threshold, expected", [
    # Casos de arredondamento (round half to even)
    # 2.225 -> 2.22 (2 é par)
    ([2.225, 100], 0, 51.11),  # (2.225 + 100) / 2 = 102.225 / 2 = 51.1125 -> 51.11
    # 2.235 -> 2.24 (3 é ímpar)
    ([2.235, 100], 0, 51.12),  # (2.235 + 100) / 2 = 102.235 / 2 = 51.1175 -> 51.12
    # 2.675 -> 2.68 (7 é ímpar)
    ([2.675, 100], 0, 51.34),  # (2.675 + 100) / 2 = 102.675 / 2 = 51.3375 -> 51.34
    # 2.685 -> 2.68 (8 é par)
    ([2.685, 100], 0, 51.34),  # (2.685 + 100) / 2 = 102.685 / 2 = 51.3425 -> 51.34
    # 0.005 -> 0.00 (0 é par)
    ([0.005, 100], 0, 50.00),  # (0.005 + 100) / 2 = 100.005 / 2 = 50.0025 -> 50.00
    # 0.015 -> 0.02 (1 é ímpar)
    ([0.015, 100], 0, 50.01),  # (0.015 + 100) / 2 = 100.015 / 2 = 50.0075 -> 50.01
])
def test_rounding_bankers_rule(values, threshold, expected):
    """
    Testa o comportamento de arredondamento para 2 casas decimais (banker's rounding).
    """
    assert average_above(values, threshold) == pytest.approx(expected)


def test_single_element_just_above_threshold_with_rounding_down():
    """
    Testa arredondamento de um único elemento que está ligeiramente acima do limiar.
    10.0049 -> 10.00
    """
    assert average_above([10.0049], 10) == pytest.approx(10.00)


def test_single_element_just_above_threshold_with_rounding_half_to_even_down():
    """
    Testa arredondamento de um único elemento que está ligeiramente acima do limiar,
    com o último dígito sendo 5 e o anterior par.
    10.005 -> 10.00 (0 é par)
    """
    assert average_above([10.005], 10) == pytest.approx(10.00)


def test_single_element_just_above_threshold_with_rounding_half_to_even_up():
    """
    Testa arredondamento de um único elemento que está ligeiramente acima do limiar,
    com o último dígito sendo 5 e o anterior ímpar.
    10.015 -> 10.02 (1 é ímpar)
    """
    assert average_above([10.015], 10) == pytest.approx(10.02)


def test_very_small_numbers_rounding_to_zero():
    """
    Testa com números muito pequenos que, após a média, arredondam para 0.00.
    (0.000002 + 0.000003) / 2 = 0.0000025 -> 0.00
    """
    assert average_above([0.000001, 0.000002, 0.000003], 0.0000015) == pytest.approx(0.00)


def test_large_number_of_elements():
    """
    Testa com uma lista grande de elementos para verificar desempenho e correção.
    Elementos > 500 são 501, ..., 1000. Soma = 375250. Contagem = 500. Média = 750.5
    """
    values = list(range(1, 1001))
    threshold = 500
    assert average_above(values, threshold) == pytest.approx(750.5)


def test_all_elements_same_and_above_threshold():
    """
    Testa quando todos os elementos são iguais e acima do limiar.
    """
    assert average_above([10.0, 10.0, 10.0], 9.9) == pytest.approx(10.0)


def test_float_threshold_integer_values():
    """
    Testa com limiar float e valores inteiros.
    Qualificados: 3, 4, 5. Soma = 12. Média = 12 / 3 = 4.0
    """
    assert average_above([1, 2, 3, 4, 5], 2.5) == pytest.approx(4.0)


def test_integer_threshold_float_values():
    """
    Testa com limiar inteiro e valores float.
    Qualificados: 3.3, 4.4, 5.5. Soma = 13.2. Média = 13.2 / 3 = 4.4
    """
    assert average_above([1.1, 2.2, 3.3, 4.4, 5.5], 3) == pytest.approx(4.4)
