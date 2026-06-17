from solution import most_visited_urls
import pytest

def test_scenario_1_n_less_than_distinct():
    """
    Cenário: Retornar as n URLs mais visitadas com n menor que o número de URLs distintas.
    Entrada: visits=["a","b","a","c","a","b"], n=2
    Esperado: ["a","b"]
    """
    visits = ["a","b","a","c","a","b"]
    n = 2
    expected = ["a","b"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_2_n_equals_one():
    """
    Cenário: Retornar apenas a URL mais visitada (n=1).
    Entrada: visits=["a","b","a","c","a","b"], n=1
    Esperado: ["a"]
    """
    visits = ["a","b","a","c","a","b"]
    n = 1
    expected = ["a"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_3_empty_visits_list():
    """
    Cenário: Lista de visitas vazia.
    Entrada: visits=[], n=5
    Esperado: []
    """
    visits = []
    n = 5
    expected = []
    assert most_visited_urls(visits, n) == expected

def test_scenario_4_n_is_zero():
    """
    Cenário: n é zero.
    Entrada: visits=["x","y"], n=0
    Esperado: []
    """
    visits = ["x","y"]
    n = 0
    expected = []
    assert most_visited_urls(visits, n) == expected

def test_scenario_5_n_is_negative():
    """
    Cenário: n é negativo.
    Entrada: visits=["x","y"], n=-1
    Esperado: []
    """
    visits = ["x","y"]
    n = -1
    expected = []
    assert most_visited_urls(visits, n) == expected

def test_scenario_6_tie_break_by_first_appearance():
    """
    Cenário: Desempate de frequência por ordem de primeira aparição.
    Entrada: visits=["b","a","a","b"], n=2
    Esperado: ["b","a"]
    """
    visits = ["b","a","a","b"]
    n = 2
    expected = ["b","a"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_7_n_greater_than_distinct_urls():
    """
    Cenário: n é maior ou igual ao número de URLs distintas.
    Entrada: visits=["a","b","a"], n=9
    Esperado: ["a","b"]
    """
    visits = ["a","b","a"]
    n = 9
    expected = ["a","b"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_8_n_less_than_distinct_varied_frequencies():
    """
    Cenário: n menor que o número de URLs distintas, com mais URLs e frequências variadas.
    Entrada: visits=["a","b","c","a","b","d","a"], n=2
    Esperado: ["a","b"]
    """
    visits = ["a","b","c","a","b","d","a"]
    n = 2
    expected = ["a","b"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_9_n_equals_distinct_urls():
    """
    Cenário: n é exatamente igual ao número de URLs distintas.
    Entrada: visits=["a","b","c","a","b","d","a"], n=4
    Esperado: ["a","b","c","d"]
    """
    visits = ["a","b","c","a","b","d","a"]
    n = 4
    expected = ["a","b","c","d"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_10_multiple_frequency_ties():
    """
    Cenário: Múltiplos empates de frequência, incluindo para posições não-top.
    Entrada: visits=["c","a","b","a","c","d","b"], n=4
    Esperado: ["c","a","b","d"]
    """
    visits = ["c","a","b","a","c","d","b"]
    n = 4
    expected = ["c","a","b","d"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_11_n_is_large_negative():
    """
    Cenário: n é um valor negativo grande.
    Entrada: visits=["x","y","z"], n=-5
    Esperado: []
    """
    visits = ["x","y","z"]
    n = -5
    expected = []
    assert most_visited_urls(visits, n) == expected

def test_scenario_12_single_distinct_url_n_equals_one():
    """
    Cenário: Lista de visitas com apenas uma URL distinta, n=1.
    Entrada: visits=["a","a","a"], n=1
    Esperado: ["a"]
    """
    visits = ["a","a","a"]
    n = 1
    expected = ["a"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_13_single_distinct_url_n_greater_than_distinct():
    """
    Cenário: Lista de visitas com apenas uma URL distinta, n maior que o número de distintas.
    Entrada: visits=["a","a","a"], n=5
    Esperado: ["a"]
    """
    visits = ["a","a","a"]
    n = 5
    expected = ["a"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_14_all_unique_urls_n_less_than_distinct():
    """
    Cenário: Todas as URLs na lista de visitas são únicas (sem repetições), n menor que o número de distintas.
    Entrada: visits=["a","b","c"], n=2
    Esperado: ["a","b"]
    """
    visits = ["a","b","c"]
    n = 2
    expected = ["a","b"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_15_all_unique_urls_n_equals_distinct():
    """
    Cenário: Todas as URLs na lista de visitas são únicas, n igual ao número de distintas.
    Entrada: visits=["a","b","c"], n=3
    Esperado: ["a","b","c"]
    """
    visits = ["a","b","c"]
    n = 3
    expected = ["a","b","c"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_16_case_sensitive_urls():
    """
    Cenário: URLs com sensibilidade a maiúsculas/minúsculas (tratadas como distintas).
    Entrada: visits=["url1","URL1","url1","url2"], n=2
    Esperado: ["url1", "URL1"]
    """
    visits = ["url1","URL1","url1","url2"]
    n = 2
    expected = ["url1", "URL1"]
    assert most_visited_urls(visits, n) == expected

def test_scenario_17_complex_dataset_n_less_than_distinct():
    """
    Cenário: Conjunto de dados mais complexo com várias URLs, frequências e empates, n menor que o número de distintas.
    Entrada: visits=["a","b","c","a","d","b","e","a","c","f","b","d","a","g","c","b","a"], n=5
    Esperado: ["a","b","c","d","e"]
    """
    visits = ["a","b","c","a","d","b","e","a","c","f","b","d","a","g","c","b","a"]
    n = 5
    expected = ["a","b","c","d","e"]
    assert most_visited_urls(visits, n) == expected
