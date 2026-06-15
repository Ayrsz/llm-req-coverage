import pytest
from solution import age_bracket

def test_age_bracket_invalid_negative_age_equivalence():
    """
    Cenário: Idade negativa (entrada inválida)
    Técnica: Classes de Equivalência (entrada inválida)
    Entrada: -5
    Resultado Esperado: "invalido"
    """
    assert age_bracket(-5) == "invalido"

def test_age_bracket_invalid_negative_age_boundary_lower():
    """
    Cenário: Idade no limite inferior da faixa inválida
    Técnica: Análise de Valores-Limite (fronteira inferior da faixa inválida)
    Entrada: -1
    Resultado Esperado: "invalido"
    """
    assert age_bracket(-1) == "invalido"

def test_age_bracket_invalid_negative_age_extreme():
    """
    Cenário: Idade negativa extrema
    Técnica: Casos de Borda / Casos Negativos
    Entrada: -999999
    Resultado Esperado: "invalido"
    """
    assert age_bracket(-999999) == "invalido"

def test_age_bracket_child_boundary_lower():
    """
    Cenário: Idade no limite inferior da faixa "criança"
    Técnica: Análise de Valores-Limite (fronteira inferior da faixa "criança")
    Entrada: 0
    Resultado Esperado: "crianca"
    """
    assert age_bracket(0) == "crianca"

def test_age_bracket_child_equivalence():
    """
    Cenário: Idade representativa da faixa "criança"
    Técnica: Classes de Equivalência (faixa "criança")
    Entrada: 5
    Resultado Esperado: "crianca"
    """
    assert age_bracket(5) == "crianca"

def test_age_bracket_child_boundary_upper():
    """
    Cenário: Idade no limite superior da faixa "criança"
    Técnica: Análise de Valores-Limite (fronteira superior da faixa "criança")
    Entrada: 11
    Resultado Esperado: "crianca"
    """
    assert age_bracket(11) == "crianca"

def test_age_bracket_teen_boundary_lower():
    """
    Cenário: Idade no limite inferior da faixa "adolescente"
    Técnica: Análise de Valores-Limite (fronteira inferior da faixa "adolescente")
    Entrada: 12
    Resultado Esperado: "adolescente"
    """
    assert age_bracket(12) == "adolescente"

def test_age_bracket_teen_equivalence():
    """
    Cenário: Idade representativa da faixa "adolescente"
    Técnica: Classes de Equivalência (faixa "adolescente")
    Entrada: 15
    Resultado Esperado: "adolescente"
    """
    assert age_bracket(15) == "adolescente"

def test_age_bracket_teen_boundary_upper():
    """
    Cenário: Idade no limite superior da faixa "adolescente"
    Técnica: Análise de Valores-Limite (fronteira superior da faixa "adolescente")
    Entrada: 17
    Resultado Esperado: "adolescente"
    """
    assert age_bracket(17) == "adolescente"

def test_age_bracket_adult_boundary_lower():
    """
    Cenário: Idade no limite inferior da faixa "adulto"
    Técnica: Análise de Valores-Limite (fronteira inferior da faixa "adulto")
    Entrada: 18
    Resultado Esperado: "adulto"
    """
    assert age_bracket(18) == "adulto"

def test_age_bracket_adult_equivalence():
    """
    Cenário: Idade representativa da faixa "adulto"
    Técnica: Classes de Equivalência (faixa "adulto")
    Entrada: 30
    Resultado Esperado: "adulto"
    """
    assert age_bracket(30) == "adulto"

def test_age_bracket_adult_boundary_upper():
    """
    Cenário: Idade no limite superior da faixa "adulto"
    Técnica: Análise de Valores-Limite (fronteira superior da faixa "adulto")
    Entrada: 59
    Resultado Esperado: "adulto"
    """
    assert age_bracket(59) == "adulto"

def test_age_bracket_elderly_boundary_lower():
    """
    Cenário: Idade no limite inferior da faixa "idoso"
    Técnica: Análise de Valores-Limite (fronteira inferior da faixa "idoso")
    Entrada: 60
    Resultado Esperado: "idoso"
    """
    assert age_bracket(60) == "idoso"

def test_age_bracket_elderly_equivalence():
    """
    Cenário: Idade representativa da faixa "idoso"
    Técnica: Classes de Equivalência (faixa "idoso")
    Entrada: 70
    Resultado Esperado: "idoso"
    """
    assert age_bracket(70) == "idoso"

def test_age_bracket_elderly_extreme():
    """
    Cenário: Idade positiva extrema (muito idoso)
    Técnica: Casos de Borda
    Entrada: 999999
    Resultado Esperado: "idoso"
    """
    assert age_bracket(999999) == "idoso"
