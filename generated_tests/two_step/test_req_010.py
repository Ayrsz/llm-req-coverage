import pytest
from solution import average_above


def test_scenario_1_empty_list():
    """Cenário 1: Lista vazia."""
    values = []
    threshold = 5.0
    expected = 0.0
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_2_no_elements_qualify_all_less_than_threshold():
    """Cenário 2: Nenhum elemento qualifica (todos menores que o limiar)."""
    values = [1, 2, 3]
    threshold = 4.0
    expected = 0.0
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_3_no_elements_qualify_all_equal_to_threshold():
    """Cenário 3: Nenhum elemento qualifica (todos iguais ao limiar)."""
    values = [5, 5, 5]
    threshold = 5.0
    expected = 0.0
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_4_no_elements_qualify_mix_less_and_equal_to_threshold():
    """Cenário 4: Nenhum elemento qualifica (mistura de menores e iguais ao limiar)."""
    values = [1, 2, 3, 3, 4]
    threshold = 4.0
    expected = 0.0
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_5_some_elements_qualify_basic_case():
    """Cenário 5: Alguns elementos qualificam (caso básico)."""
    values = [1, 2, 3, 4]
    threshold = 2.0
    expected = 3.5
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_6_all_elements_qualify():
    """Cenário 6: Todos os elementos qualificam."""
    values = [10, 20, 30]
    threshold = 5.0
    expected = 20.00
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_7_only_one_element_qualifies():
    """Cenário 7: Apenas um elemento qualifica."""
    values = [1, 2, 10, 3, 4]
    threshold = 9.0
    expected = 10.00
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_8_element_exactly_at_threshold_is_discarded():
    """Cenário 8: Elemento exatamente no limiar é descartado."""
    values = [10]
    threshold = 10.0
    expected = 0.0
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_9_element_slightly_above_threshold_qualifies():
    """Cenário 9: Elemento ligeiramente acima do limiar qualifica."""
    values = [9.99, 10.0, 10.0001, 10.01]
    threshold = 10.0
    expected = 10.01
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_10_element_slightly_below_threshold_does_not_qualify():
    """Cenário 10: Elemento ligeiramente abaixo do limiar não qualifica."""
    values = [9.99, 10.0, 10.01]
    threshold = 10.0
    expected = 10.01
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_11_rounding_half_to_even_even_last_digit():
    """Cenário 11: Arredondamento (round half to even - dígito final par)."""
    values = [1.005, 2.005]
    threshold = 0.0
    expected = 1.50
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_12_rounding_half_to_even_odd_last_digit():
    """Cenário 12: Arredondamento (round half to even - dígito final ímpar)."""
    values = [1.015, 2.015]
    threshold = 0.0
    expected = 1.52
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_13_rounding_more_than_2_decimal_places_rounds_down():
    """Cenário 13: Arredondamento (mais de 2 casas decimais, arredonda para baixo)."""
    values = [1.111, 2.222, 3.333]
    threshold = 0.0
    expected = 2.22
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_14_rounding_result_with_2_exact_decimals_but_5_in_third_place():
    """Cenário 14: Arredondamento (resultado com 2 casas exatas, mas com 5 na terceira casa)."""
    values = [1.23, 4.56]
    threshold = 0.0
    expected = 2.90
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_15_rounding_result_with_1_decimal_place_should_add_zero():
    """Cenário 15: Arredondamento (resultado com 1 casa decimal, deve adicionar zero)."""
    values = [1.5, 2.5]
    threshold = 0.0
    expected = 2.00
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_16_values_with_negative_numbers_positive_threshold():
    """Cenário 16: `values` com números negativos, `threshold` positivo."""
    values = [-5, -2, 0, 1, 3]
    threshold = 0.0
    expected = 2.00
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_17_values_with_positive_numbers_negative_threshold():
    """Cenário 17: `values` com números positivos, `threshold` negativo."""
    values = [1, 2, 3, 4]
    threshold = -5.0
    expected = 2.50
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_18_values_and_threshold_negative_some_qualify():
    """Cenário 18: `values` e `threshold` negativos (alguns qualificam)."""
    values = [-10, -5, -2, 0, 5]
    threshold = -3.0
    expected = 1.00
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_19_values_and_threshold_negative_none_qualify():
    """Cenário 19: `values` e `threshold` negativos (nenhum qualifica)."""
    values = [-10, -5, -2]
    threshold = -1.0
    expected = 0.0
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_20_values_with_large_numbers():
    """Cenário 20: `values` com números grandes."""
    values = [1000000, 2000000, 3000000]
    threshold = 1500000.0
    expected = 2500000.00
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_21_values_with_small_numbers_near_zero():
    """Cenário 21: `values` com números pequenos (próximos de zero)."""
    values = [0.001, 0.002, 0.003]
    threshold = 0.0015
    expected = 0.00
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_22_all_identical_elements_qualify():
    """Cenário 22: Todos os elementos idênticos e qualificam."""
    values = [7.7, 7.7, 7.7]
    threshold = 7.0
    expected = 7.70
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_23_threshold_is_zero_values_contains_zero():
    """Cenário 23: `threshold` é zero, `values` contém zero."""
    values = [-1, 0, 1, 2]
    threshold = 0.0
    expected = 1.50
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_24_values_with_mix_of_int_and_float():
    """Cenário 24: `values` com mistura de `int` e `float`."""
    values = [1, 2.5, 3, 4.5]
    threshold = 2.0
    expected = 3.33
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_25_threshold_is_large_negative_number():
    """Cenário 25: `threshold` é um número grande negativo."""
    values = [-10, 0, 10]
    threshold = -1000.0
    expected = 0.00
    assert average_above(values, threshold) == pytest.approx(expected)


def test_scenario_26_threshold_is_large_positive_number():
    """Cenário 26: `threshold` é um número grande positivo."""
    values = [10, 100, 1000]
    threshold = 5000.0
    expected = 0.0
    assert average_above(values, threshold) == pytest.approx(expected)
