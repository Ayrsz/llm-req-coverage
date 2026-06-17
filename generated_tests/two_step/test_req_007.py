import pytest
from solution import slugify

# 1. Classes de Equivalência (Equivalence Partitioning)
@pytest.mark.parametrize(
    "text, expected_slug",
    [
        # Entradas Válidas
        pytest.param("hello-world-123", "hello-world-123", id="EQ-01: Texto já canônico"),
        pytest.param("simples", "simples", id="EQ-02: Apenas letras minúsculas"),
        pytest.param("12345", "12345", id="EQ-03: Apenas dígitos"),
        pytest.param("texto123", "texto123", id="EQ-04: Letras e dígitos"),
        pytest.param("hello world", "hello-world", id="EQ-05: Texto com espaços (AC2)"),
        pytest.param("foo_bar", "foo-bar", id="EQ-06: Texto com underscores (AC3)"),
        pytest.param("São Paulo", "sao-paulo", id="EQ-07: Texto com acentos comuns (AC6)"),
        pytest.param("Français e Español", "francais-e-espanol", id="EQ-08: Texto com acentos menos comuns (ç, ñ)"),
        pytest.param("æther", "aether", id="EQ-09: Caracteres que se decompõem em múltiplos ASCII alfanuméricos (æ)"),
        pytest.param("Trademark™", "trademarktm", id="EQ-10: Caracteres que se decompõem em ASCII alfanumérico (™ -> TM)"),
        pytest.param("Copyright©", "copyrightc", id="EQ-11: Caracteres que se decompõem em ASCII alfanumérico com pontuação intermediária (© -> (c))"),
        pytest.param("Hello, World!", "hello-world", id="EQ-12: Texto com pontuação (AC1)"),
        pytest.param("Product #123", "product-123", id="EQ-13: Texto com símbolos especiais"),
        pytest.param("HeLlO WoRlD", "hello-world", id="EQ-14: Texto com maiúsculas e minúsculas"),
        pytest.param("  Olá, Mundo! 123_abc  ", "ola-mundo-123-abc", id="EQ-15: Combinação de várias transformações"),

        # Entradas Degeneradas (Casos Negativos)
        pytest.param("", "", id="EQ-16: String vazia (AC7)"),
        pytest.param("   ", "", id="EQ-17: Apenas espaços"),
        pytest.param("___", "", id="EQ-18: Apenas underscores"),
        pytest.param("---", "", id="EQ-19: Apenas hifens"),
        pytest.param(",./;'", "", id="EQ-20: Apenas pontuação"),
        pytest.param("!@#$%^&*", "", id="EQ-21: Apenas símbolos (AC8)"),
        pytest.param("😀😂👍", "", id="EQ-22: Apenas emojis"),
        pytest.param("你好世界", "", id="EQ-23: Apenas ideogramas"),
        pytest.param("  _!@#$😀  ", "", id="EQ-24: Mistura de caracteres não-slug"),
        pytest.param("Straße", "strae", id="EQ-25: Caracteres que não se decompõem em ASCII alfanumérico e são removidos (ß)"),
    ],
)
def test_equivalence_partitioning(text, expected_slug):
    assert slugify(text) == expected_slug

# 2. Análise de Valores-Limite (Boundary Value Analysis)
@pytest.mark.parametrize(
    "text, expected_slug",
    [
        pytest.param("a", "a", id="BV-01: String de um caractere válido"),
        pytest.param("A", "a", id="BV-02: String de um caractere maiúsculo"),
        pytest.param("1", "1", id="BV-03: String de um dígito"),
        pytest.param(" ", "", id="BV-04: String de um espaço"),
        pytest.param("_", "", id="BV-05: String de um underscore"),
        pytest.param("-", "", id="BV-06: String de um hífen"),
        pytest.param("!", "", id="BV-07: String de um símbolo"),
        pytest.param("á", "a", id="BV-08: String de um caractere acentuado"),
        pytest.param("ß", "", id="BV-09: String de um caractere ß (removido)"),
        pytest.param("æ", "ae", id="BV-10: String de um caractere æ (decomposto)"),
        pytest.param("ab", "ab", id="BV-11: String de dois caracteres válidos"),
        pytest.param("  ", "", id="BV-12: String de dois espaços"),
        pytest.param("__", "", id="BV-13: String de dois underscores"),
        pytest.param("--", "", id="BV-14: String de dois hifens"),
        pytest.param("áá", "aa", id="BV-15: String de dois caracteres acentuados"),
        pytest.param(" hello", "hello", id="BV-16: String com espaço no início"),
        pytest.param("hello ", "hello", id="BV-17: String com espaço no fim"),
        pytest.param("_hello", "hello", id="BV-18: String com underscore no início"),
        pytest.param("hello_", "hello", id="BV-19: String com underscore no fim"),
        pytest.param("!hello", "hello", id="BV-20: String com pontuação no início"),
        pytest.param("hello!", "hello", id="BV-21: String com pontuação no fim"),
    ],
)
def test_boundary_value_analysis(text, expected_slug):
    assert slugify(text) == expected_slug

# 3. Casos de Borda e Invariantes (Edge Cases & Invariants)
@pytest.mark.parametrize(
    "text, expected_slug",
    [
        pytest.param("Hello   World", "hello-world", id="EC-01: Múltiplos espaços consecutivos"),
        pytest.param("foo___bar", "foo-bar", id="EC-02: Múltiplos underscores consecutivos"),
        pytest.param("foo _  _ bar", "foo-bar", id="EC-03: Mistura de separadores consecutivos"),
        pytest.param("a---b", "a-b", id="EC-04: Hifens consecutivos (AC4)"),
        pytest.param("a - _ - b", "a-b", id="EC-05: Hifens resultantes de separadores e hifens"),
        pytest.param("-hello-world-", "hello-world", id="EC-06: Hifens no início e fim (AC5)"),
        pytest.param("---hello-world---", "hello-world", id="EC-07: Múltiplos hifens no início e fim"),
        pytest.param("  _!@#$Hello World!@#$_  ", "hello-world", id="EC-08: Espaços/underscores/pontuação que viram hifens e são aparados"),
        pytest.param("  - _ -  ", "", id="EC-09: String que se torna apenas hifens e é aparada para vazio"),
        pytest.param("\x00\x01\x02", "", id="EC-10: Caracteres de controle Unicode"),
        pytest.param("\u00a0Hello\u2003World\u00a0", "hello-world", id="EC-11: Espaços Unicode não-quebráveis e outros"),
        pytest.param("Testando 123 com Áçêñtøs e Símbølôs!@#$", "testando-123-com-acentos-e-simbolos", id="EC-12: Invariante - Resultado contém apenas [a-z0-9-]"),
        pytest.param("Python 3.10", "python-310", id="EC-13: Critério de Aceitação AC9"),
    ],
)
def test_edge_cases_and_invariants(text, expected_slug):
    result = slugify(text)
    assert result == expected_slug
    # Invariantes adicionais para verificar a estrutura do slug
    if expected_slug != "":
        assert result[0] != '-', f"Slug '{result}' não deve começar com hífen."
        assert result[-1] != '-', f"Slug '{result}' não deve terminar com hífen."
        assert '--' not in result, f"Slug '{result}' não deve conter hifens consecutivos."
    assert all(c.isalnum() or c == '-' for c in result), f"Slug '{result}' contém caracteres inválidos."
