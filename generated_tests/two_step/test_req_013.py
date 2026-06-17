import pytest
from solution import shipping_cost

def test_weight_zero_returns_zero():
    """
    Cenário 1: weight = 0, region = "sul", express = False -> 0.0
    Técnica: Casos Negativos / Entradas Inválidas (weight <= 0)
    """
    assert shipping_cost(0, "sul", False) == 0.0

def test_weight_negative_integer_returns_zero():
    """
    Cenário 2: weight = -1, region = "norte", express = True -> 0.0 (AC6)
    Técnica: Casos Negativos / Entradas Inválidas (weight < 0)
    """
    assert shipping_cost(-1, "norte", True) == 0.0

def test_weight_negative_float_returns_zero():
    """
    Cenário 3: weight = -0.001, region = "centro-oeste", express = False -> 0.0
    Técnica: Casos Negativos / Entradas Inválidas (weight < 0, float)
    """
    assert shipping_cost(-0.001, "centro-oeste", False) == 0.0

def test_weight_five_sul_no_express_returns_base_sul():
    """
    Cenário 4: weight = 5, region = "sul", express = False -> 10.0 (AC1)
    Técnica: Análise de Valores-Limite (weight = 5, sem adicional, região barata, sem express)
    """
    assert shipping_cost(5, "sul", False) == 10.0

def test_weight_five_norte_no_express_returns_base_norte():
    """
    Cenário 5: weight = 5, region = "norte", express = False -> 20.0 (AC2)
    Técnica: Análise de Valores-Limite (weight = 5, sem adicional, região cara, sem express)
    """
    assert shipping_cost(5, "norte", False) == 20.0

def test_weight_five_unknown_region_express_returns_base_unknown_express():
    """
    Cenário 6: weight = 5, region = "desconhecida", express = True -> 37.5 (25.0 * 1.5)
    Técnica: Análise de Valores-Limite (weight = 5, sem adicional, região desconhecida, com express)
    """
    assert shipping_cost(5, "desconhecida", True) == pytest.approx(37.5)

def test_weight_less_than_five_sudeste_no_express_returns_base_sudeste():
    """
    Cenário 7: weight = 3, region = "sudeste", express = False -> 10.0
    Técnica: Classes de Equivalência (weight < 5, região barata, sem express)
    """
    assert shipping_cost(3, "sudeste", False) == 10.0

def test_weight_less_than_five_nordeste_express_returns_base_nordeste_express():
    """
    Cenário 8: weight = 4.5, region = "nordeste", express = True -> 30.0 (20.0 * 1.5)
    Técnica: Classes de Equivalência (weight < 5, região cara, com express)
    """
    assert shipping_cost(4.5, "nordeste", True) == pytest.approx(30.0)

def test_weight_less_than_five_unknown_region_no_express_returns_base_unknown():
    """
    Cenário 9: weight = 3, region = "marte", express = False -> 25.0 (AC5)
    Técnica: Classes de Equivalência (weight < 5, região desconhecida, sem express)
    """
    assert shipping_cost(3, "marte", False) == 25.0

def test_weight_just_above_five_sul_no_express_applies_small_additional():
    """
    Cenário 10: weight = 5.01, region = "sul", express = False -> 10.02 (10 + 0.01 * 2)
    Técnica: Análise de Valores-Limite (weight > 5, apenas acima do limite, região barata, sem express)
    """
    assert shipping_cost(5.01, "sul", False) == pytest.approx(10.02)

def test_weight_just_above_five_sul_express_applies_small_additional_and_express():
    """
    Cenário 11: weight = 5.01, region = "sul", express = True -> 15.03 (10.02 * 1.5)
    Técnica: Análise de Valores-Limite (weight > 5, apenas acima do limite, região barata, com express)
    """
    assert shipping_cost(5.01, "sul", True) == pytest.approx(15.03)

def test_weight_above_five_sudeste_no_express_applies_additional():
    """
    Cenário 12: weight = 6, region = "sudeste", express = False -> 12.0 (AC3)
    Técnica: Classes de Equivalência (weight > 5, peso inteiro, região barata, sem express)
    """
    assert shipping_cost(6, "sudeste", False) == pytest.approx(12.0)

def test_weight_above_five_sul_express_applies_additional_and_express():
    """
    Cenário 13: weight = 6, region = "sul", express = True -> 18.0 (AC4)
    Técnica: Classes de Equivalência (weight > 5, peso inteiro, região barata, com express)
    """
    assert shipping_cost(6, "sul", True) == pytest.approx(18.0)

def test_weight_above_five_norte_no_express_applies_additional():
    """
    Cenário 14: weight = 7, region = "norte", express = False -> 24.0 (20 + (7 - 5) * 2)
    Técnica: Classes de Equivalência (weight > 5, peso inteiro, região cara, sem express)
    """
    assert shipping_cost(7, "norte", False) == pytest.approx(24.0)

def test_weight_above_five_nordeste_express_applies_additional_and_express():
    """
    Cenário 15: weight = 10, region = "nordeste", express = True -> 45.0 (AC7)
    Técnica: Classes de Equivalência (weight > 5, peso inteiro, região cara, com express)
    """
    assert shipping_cost(10, "nordeste", True) == pytest.approx(45.0)

def test_weight_above_five_unknown_region_no_express_applies_additional():
    """
    Cenário 16: weight = 8, region = "outro_lugar", express = False -> 31.0 (25 + (8 - 5) * 2)
    Técnica: Classes de Equivalência (weight > 5, peso inteiro, região desconhecida, sem express)
    """
    assert shipping_cost(8, "outro_lugar", False) == pytest.approx(31.0)

def test_rounding_half_up_with_express():
    """
    Cenário 17: weight = 5.005, region = "sul", express = True -> 15.02
    Técnica: Casos de Borda / Arredondamento (valor final .XX5, arredonda para cima)
    """
    # (10 + (5.005 - 5) * 2) * 1.5 = (10 + 0.01) * 1.5 = 10.01 * 1.5 = 15.015 -> 15.02
    assert shipping_cost(5.005, "sul", True) == pytest.approx(15.02)

def test_rounding_half_down_with_express():
    """
    Cenário 18: weight = 5.004, region = "sul", express = True -> 15.01
    Técnica: Casos de Borda / Arredondamento (valor final .XX4, arredonda para baixo)
    """
    # (10 + (5.004 - 5) * 2) * 1.5 = (10 + 0.008) * 1.5 = 10.008 * 1.5 = 15.012 -> 15.01
    assert shipping_cost(5.004, "sul", True) == pytest.approx(15.01)

def test_rounding_many_decimals_no_express():
    """
    Cenário 19: weight = 5.12345, region = "sul", express = False -> 10.25
    Técnica: Casos de Borda / Arredondamento (valor intermediário com muitas casas decimais)
    """
    # 10 + (5.12345 - 5) * 2 = 10 + 0.12345 * 2 = 10 + 0.2469 = 10.2469 -> 10.25
    assert shipping_cost(5.12345, "sul", False) == pytest.approx(10.25)

def test_rounding_many_decimals_with_express():
    """
    Cenário 20: weight = 5.12345, region = "sul", express = True -> 15.37
    Técnica: Casos de Borda / Arredondamento (valor intermediário com muitas casas decimais e express)
    """
    # (10 + (5.12345 - 5) * 2) * 1.5 = (10 + 0.2469) * 1.5 = 10.2469 * 1.5 = 15.37035 -> 15.37
    assert shipping_cost(5.12345, "sul", True) == pytest.approx(15.37)

def test_region_case_sensitive_returns_unknown_base():
    """
    Cenário 21: weight = 1, region = "Sul", express = False -> 25.0
    Técnica: Casos de Borda / Entradas Inválidas (região case-sensitive)
    """
    assert shipping_cost(1, "Sul", False) == 25.0

def test_region_with_spaces_returns_unknown_base():
    """
    Cenário 22: weight = 1, region = " sudeste ", express = False -> 25.0
    Técnica: Casos de Borda / Entradas Inválidas (região com espaços)
    """
    assert shipping_cost(1, " sudeste ", False) == 25.0

def test_region_empty_string_returns_unknown_base():
    """
    Cenário 23: weight = 1, region = "", express = False -> 25.0
    Técnica: Casos de Borda / Entradas Inválidas (região string vazia)
    """
    assert shipping_cost(1, "", False) == 25.0

def test_weight_just_below_five_no_additional():
    """
    Cenário 24: weight = 4.99, region = "sul", express = False -> 10.0
    Técnica: Invariantes (custo não-decrescente com peso)
    """
    assert shipping_cost(4.99, "sul", False) == 10.0

def test_express_mode_is_never_cheaper():
    """
    Cenário 25: Invariantes (express=True nunca mais barato que express=False)
    Entrada: weight = 7, region = "centro-oeste", express = False -> 24.0
    Entrada: weight = 7, region = "centro-oeste", express = True -> 36.0
    """
    cost_no_express = shipping_cost(7, "centro-oeste", False)
    cost_express = shipping_cost(7, "centro-oeste", True)
    assert cost_no_express == pytest.approx(24.0)
    assert cost_express == pytest.approx(36.0)
    assert cost_express > cost_no_express
