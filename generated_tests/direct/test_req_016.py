import pytest
from solution import most_visited_urls

def test_ac1_basic_ranking():
    """AC1. most_visited_urls(["a","b","a","c","a","b"], 2) == ["a","b"] (a=3, b=2, c=1)."""
    visits = ["a", "b", "a", "c", "a", "b"]
    n = 2
    expected = ["a", "b"]
    assert most_visited_urls(visits, n) == expected

def test_ac2_single_most_visited():
    """AC2. most_visited_urls(["a","b","a","c","a","b"], 1) == ["a"]."""
    visits = ["a", "b", "a", "c", "a", "b"]
    n = 1
    expected = ["a"]
    assert most_visited_urls(visits, n) == expected

def test_ac3_empty_visits_list():
    """AC3. most_visited_urls([], 5) == []."""
    visits = []
    n = 5
    expected = []
    assert most_visited_urls(visits, n) == expected

@pytest.mark.parametrize("n_value", [0, -1, -5])
def test_ac4_n_zero_or_negative(n_value):
    """AC4. most_visited_urls(["x","y"], 0) == [] e most_visited_urls(["x","y"], -1) == [].
    Também cobre casos de n negativo."""
    visits = ["x", "y", "z"]
    expected = []
    assert most_visited_urls(visits, n_value) == expected

def test_ac5_tie_breaking_first_appearance():
    """AC5. Desempate por primeira aparição: most_visited_urls(["b","a","a","b"], 2) == ["b","a"]
    (b e a têm freq 2; b apareceu primeiro)."""
    visits = ["b", "a", "a", "b"]
    n = 2
    expected = ["b", "a"]
    assert most_visited_urls(visits, n) == expected

def test_ac6_n_greater_than_distinct_urls():
    """AC6. n maior que distintas: most_visited_urls(["a","b","a"], 9) == ["a","b"]."""
    visits = ["a", "b", "a"]
    n = 9
    expected = ["a", "b"]
    assert most_visited_urls(visits, n) == expected

def test_typical_multiple_urls_different_frequencies():
    """Caso típico com múltiplas URLs e frequências variadas."""
    visits = ["home", "about", "home", "contact", "home", "about", "products"]
    n = 3
    # home: 3 (primeira em 0)
    # about: 2 (primeira em 1)
    # contact: 1 (primeira em 3)
    # products: 1 (primeira em 6)
    expected = ["home", "about", "contact"]
    assert most_visited_urls(visits, n) == expected

def test_typical_all_urls_same_frequency():
    """Caso típico onde todas as URLs têm a mesma frequência, desempate por primeira aparição."""
    visits = ["a", "b", "c", "a", "b", "c"]
    n = 3
    # a: 2 (primeira em 0)
    # b: 2 (primeira em 1)
    # c: 2 (primeira em 2)
    expected = ["a", "b", "c"]
    assert most_visited_urls(visits, n) == expected

def test_typical_all_urls_same_frequency_truncated():
    """Caso típico com todas as URLs na mesma frequência, mas `n` trunca o resultado."""
    visits = ["a", "b", "c", "a", "b", "c"]
    n = 2
    expected = ["a", "b"]
    assert most_visited_urls(visits, n) == expected

def test_edge_n_equals_distinct_count():
    """Valor-limite: `n` é igual ao número de URLs distintas."""
    visits = ["x", "y", "z", "x", "y"]
    n = 3
    # x: 2 (primeira em 0)
    # y: 2 (primeira em 1)
    # z: 1 (primeira em 2)
    expected = ["x", "y", "z"]
    assert most_visited_urls(visits, n) == expected

def test_edge_single_url_multiple_visits():
    """Valor-limite: Apenas uma URL distinta, visitada múltiplas vezes."""
    visits = ["google.com", "google.com", "google.com"]
    n = 1
    expected = ["google.com"]
    assert most_visited_urls(visits, n) == expected

def test_edge_single_url_multiple_visits_n_greater():
    """Valor-limite: Apenas uma URL distinta, `n` maior que 1."""
    visits = ["google.com", "google.com", "google.com"]
    n = 5
    expected = ["google.com"]
    assert most_visited_urls(visits, n) == expected

def test_edge_single_distinct_url():
    """Valor-limite: Apenas uma URL distinta, visitada uma vez."""
    visits = ["only.com"]
    n = 1
    expected = ["only.com"]
    assert most_visited_urls(visits, n) == expected

def test_edge_single_distinct_url_n_greater():
    """Valor-limite: Apenas uma URL distinta, visitada uma vez, `n` maior que 1."""
    visits = ["only.com"]
    n = 5
    expected = ["only.com"]
    assert most_visited_urls(visits, n) == expected

def test_edge_single_distinct_url_n_is_zero():
    """Valor-limite: Apenas uma URL distinta, `n` é zero."""
    visits = ["a", "a", "a"]
    n = 0
    expected = []
    assert most_visited_urls(visits, n) == expected

def test_invalid_single_distinct_url_n_is_negative():
    """Caso inválido: Apenas uma URL distinta, `n` é negativo."""
    visits = ["a", "a", "a"]
    n = -3
    expected = []
    assert most_visited_urls(visits, n) == expected

def test_urls_with_paths_and_domains():
    """Caso com URLs mais complexas (domínios e caminhos)."""
    visits = [
        "https://www.example.com/page1",
        "https://www.example.com/page2",
        "https://www.example.com/page1",
        "https://www.anothersite.org",
        "https://www.example.com/page1",
        "https://www.anothersite.org",
    ]
    n = 2
    # page1: 3 (primeira em 0)
    # anothersite: 2 (primeira em 3)
    # page2: 1 (primeira em 1)
    expected = ["https://www.example.com/page1", "https://www.anothersite.org"]
    assert most_visited_urls(visits, n) == expected

def test_urls_with_different_schemes_and_subdomains():
    """Caso com URLs com esquemas e subdomínios diferentes, incluindo desempate."""
    visits = [
        "http://blog.example.com",
        "https://blog.example.com",
        "http://blog.example.com",
        "https://www.example.com",
    ]
    n = 3
    # http://blog.example.com: 2 (primeira em 0)
    # https://blog.example.com: 1 (primeira em 1)
    # https://www.example.com: 1 (primeira em 3)
    expected = ["http://blog.example.com", "https://blog.example.com", "https://www.example.com"]
    assert most_visited_urls(visits, n) == expected

def test_many_distinct_urls_truncated():
    """Caso com muitas URLs distintas, `n` trunca o resultado."""
    visits = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    n = 5
    expected = ["a", "b", "c", "d", "e"]
    assert most_visited_urls(visits, n) == expected

def test_many_distinct_urls_all():
    """Caso com muitas URLs distintas, `n` é maior que o número de distintas."""
    visits = ["a", "b", "c", "d", "e"]
    n = 10
    expected = ["a", "b", "c", "d", "e"]
    assert most_visited_urls(visits, n) == expected

def test_complex_tie_breaking():
    """Caso complexo de desempate por primeira aparição com múltiplas frequências."""
    visits = [
        "url_c", "url_a", "url_b", "url_a", "url_c", "url_b", "url_d", "url_a"
    ]
    n = 4
    # url_a: 3 (primeira em 1)
    # url_c: 2 (primeira em 0)
    # url_b: 2 (primeira em 2)
    # url_d: 1 (primeira em 6)
    expected = ["url_a", "url_c", "url_b", "url_d"]
    assert most_visited_urls(visits, n) == expected

def test_complex_tie_breaking_truncated():
    """Caso complexo de desempate, com `n` truncando o resultado."""
    visits = [
        "url_c", "url_a", "url_b", "url_a", "url_c", "url_b", "url_d", "url_a"
    ]
    n = 2
    expected = ["url_a", "url_c"]
    assert most_visited_urls(visits, n) == expected

@pytest.mark.parametrize("n_value", [0, -1, -5])
def test_empty_visits_n_zero_or_negative(n_value):
    """Caso de borda: lista de visitas vazia com `n` zero ou negativo."""
    visits = []
    expected = []
    assert most_visited_urls(visits, n_value) == expected

def test_large_number_of_visits():
    """Teste com um grande número de visitas para verificar desempenho básico."""
    visits = ["a"] * 1000 + ["b"] * 500 + ["c"] * 200 + ["d"] * 100
    n = 3
    expected = ["a", "b", "c"]
    assert most_visited_urls(visits, n) == expected

def test_large_number_of_visits_with_ties():
    """Teste com um grande número de visitas e empates."""
    visits = ["a"] * 100 + ["b"] * 100 + ["c"] * 50 + ["d"] * 50 + ["e"] * 10
    n = 4
    expected = ["a", "b", "c", "d"]
    assert most_visited_urls(visits, n) == expected

def test_numeric_urls_as_strings():
    """Teste com URLs que são números representados como strings."""
    visits = ["1", "2", "1", "3", "1", "2"]
    n = 2
    expected = ["1", "2"]
    assert most_visited_urls(visits, n) == expected

def test_urls_with_spaces_and_special_chars():
    """Teste com URLs contendo espaços e caracteres especiais."""
    visits = ["my page", "my page", "another page!", "my page", "another page!"]
    n = 2
    expected = ["my page", "another page!"]
    assert most_visited_urls(visits, n) == expected

def test_urls_with_mixed_case():
    """Teste com URLs que diferem apenas por caixa (case-sensitive)."""
    visits = ["page", "Page", "page", "PAGE"]
    n = 3
    # page: 2 (primeira em 0)
    # Page: 1 (primeira em 1)
    # PAGE: 1 (primeira em 3)
    expected = ["page", "Page", "PAGE"]
    assert most_visited_urls(visits, n) == expected
