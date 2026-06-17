from solution import most_frequent

def test_empty_list():
    """
    Técnica: Classes de Equivalência / Valores-Limite / Casos de Borda / Critério de Aceitação (AC2)
    Comentário: Lista de entrada vazia.
    """
    assert most_frequent([]) == ""

def test_single_element_list():
    """
    Técnica: Classes de Equivalência / Valores-Limite / Casos de Borda / Critério de Aceitação (AC5)
    Comentário: Lista com um único elemento.
    """
    assert most_frequent(["x"]) == "x"

def test_isolated_winner_by_frequency():
    """
    Técnica: Classes de Equivalência / Critério de Aceitação (AC1)
    Comentário: Um vencedor isolado por frequência (frequência de "a" é 2, "b" é 1).
    """
    assert most_frequent(["a", "b", "a"]) == "a"

def test_frequency_tie_first_occurrence_simple():
    """
    Técnica: Classes de Equivalência / Valores-Limite / Critério de Aceitação (AC3)
    Comentário: Empate de frequência (ambos 1), desempate pela primeira ocorrência ("a" aparece no índice 0).
    """
    assert most_frequent(["a", "b"]) == "a"

def test_frequency_tie_first_occurrence_complex():
    """
    Técnica: Classes de Equivalência / Valores-Limite / Critério de Aceitação (AC4)
    Comentário: Empate de frequência (ambos 2), desempate pela primeira ocorrência ("b" aparece no índice 0).
    """
    assert most_frequent(["b", "a", "a", "b"]) == "b"

def test_frequency_tie_example_xyxy():
    """
    Técnica: Classes de Equivalência / Exemplo do Requisito
    Comentário: Empate de frequência (ambos 2), desempate pela primeira ocorrência ("x" aparece no índice 0).
    """
    assert most_frequent(["x", "y", "x", "y"]) == "x"

def test_frequency_tie_example_yxyx():
    """
    Técnica: Classes de Equivalência / Exemplo do Requisito
    Comentário: Empate de frequência (ambos 2), desempate pela primeira ocorrência ("y" aparece no índice 0).
    """
    assert most_frequent(["y", "x", "y", "x"]) == "y"

def test_all_distinct_elements():
    """
    Técnica: Classes de Equivalência / Exemplo do Requisito
    Comentário: Todos os elementos distintos (frequência 1), desempate pela primeira ocorrência ("c" aparece no índice 0).
    """
    assert most_frequent(["c", "b", "a"]) == "c"

def test_all_elements_identical():
    """
    Técnica: Classes de Equivalência / Casos de Borda
    Comentário: Todos os elementos da lista são idênticos.
    """
    assert most_frequent(["a", "a", "a", "a"]) == "a"

def test_multiple_elements_clear_winner():
    """
    Técnica: Classes de Equivalência
    Comentário: Múltiplos elementos com frequências variadas, um vencedor claro por frequência ("apple" com 3 ocorrências).
    """
    assert most_frequent(["apple", "banana", "apple", "orange", "apple", "banana"]) == "apple"

def test_three_way_frequency_tie():
    """
    Técnica: Classes de Equivalência / Casos de Borda
    Comentário: Empate de frequência entre três elementos ("a", "b", "c" com 2 ocorrências), desempate pela primeira ocorrência ("a" aparece no índice 0).
    """
    assert most_frequent(["a", "b", "c", "a", "b", "c", "d"]) == "a"

def test_four_way_frequency_tie():
    """
    Técnica: Classes de Equivalência / Casos de Borda
    Comentário: Empate de frequência entre quatro elementos ("a", "b", "c", "d" com 2 ocorrências), desempate pela primeira ocorrência ("d" aparece no índice 0).
    """
    assert most_frequent(["d", "a", "b", "c", "a", "b", "c", "d", "e"]) == "d"

def test_empty_strings_as_elements():
    """
    Técnica: Casos de Borda
    Comentário: Strings vazias como elementos da lista, sendo a mais frequente.
    """
    assert most_frequent(["", "a", "", "b", "c", ""]) == ""

def test_special_characters():
    """
    Técnica: Casos de Borda
    Comentário: Strings contendo caracteres especiais, com um vencedor por frequência.
    """
    assert most_frequent(["!", "@", "!", "#", "@", "!"]) == "!"

def test_alphanumeric_strings():
    """
    Técnica: Casos de Borda
    Comentário: Strings contendo números e letras, com um vencedor por frequência.
    """
    assert most_frequent(["123", "abc", "123", "xyz", "abc", "123"]) == "123"

def test_case_sensitivity():
    """
    Técnica: Casos de Borda
    Comentário: Teste de sensibilidade a maiúsculas/minúsculas. "a" (3 ocorrências, primeira no índice 0) vs "A" (2 ocorrências, primeira no índice 1).
    """
    assert most_frequent(["a", "A", "a", "B", "A", "a"]) == "a"

def test_long_list_all_distinct():
    """
    Técnica: Invariantes / Casos de Borda
    Comentário: Lista longa com todos os elementos distintos, o primeiro elemento é o vencedor.
    """
    long_list = ["z", "y", "x", "w", "v", "u", "t", "s", "r", "q", "p", "o", "n", "m", "l", "k", "j", "i", "h", "g", "f", "e", "d", "c", "b", "a"]
    assert most_frequent(long_list) == "z"

def test_long_strings_as_elements():
    """
    Técnica: Invariantes / Casos de Borda
    Comentário: Strings longas como elementos, com um vencedor por frequência.
    """
    assert most_frequent(["long_string_1", "long_string_2", "long_string_1", "long_string_3", "long_string_2", "long_string_1"]) == "long_string_1"
