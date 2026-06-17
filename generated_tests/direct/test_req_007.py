import pytest
from solution import slugify

# Testes baseados nos Critérios de Aceitação (ACs)
def test_slugify_acceptance_criteria():
    assert slugify("  Olá, Mundo! ") == "ola-mundo"  # AC1
    assert slugify("Hello World") == "hello-world"    # AC2
    assert slugify("foo_bar") == "foo-bar"            # AC3
    assert slugify("a---b") == "a-b"                  # AC4
    assert slugify("-already-slug-") == "already-slug" # AC5
    assert slugify("Café com Leite") == "cafe-com-leite" # AC6
    assert slugify("") == ""                          # AC7
    assert slugify("!!!") == ""                       # AC8
    assert slugify("Python 3.10") == "python-310"     # AC9

# Testes de casos típicos e classes de equivalência
@pytest.mark.parametrize(
    "input_text, expected_slug",
    [
        # Texto alfanumérico simples
        ("simple text", "simple-text"),
        ("Another Simple Text", "another-simple-text"),
        ("123abcDEF", "123abcdef"),
        ("already-a-slug", "already-a-slug"),

        # Texto com espaços/underscores
        ("foo bar baz", "foo-bar-baz"),
        ("foo_bar_baz", "foo-bar-baz"),
        ("foo bar_baz", "foo-bar-baz"),
        ("foo   bar   baz", "foo-bar-baz"), # Múltiplos espaços
        ("foo___bar___baz", "foo-bar-baz"), # Múltiplos underscores
        ("foo _ bar", "foo-bar"),           # Mistura de separadores

        # Texto com acentos (normalização NFKD)
        ("São Paulo", "sao-paulo"),
        ("Mañana", "manana"),
        ("Français", "francais"),
        ("Müller", "muller"),
        ("Coração", "coracao"),
        ("L'Hôpital", "lhopital"),

        # Texto com pontuação/símbolos
        ("Hello, World!", "hello-world"),
        ("What's up?", "whats-up"),
        ("User@Domain.com", "userdomaincom"),
        ("Product #123", "product-123"),
        ("100% discount", "100-discount"),
        ("R$ 1.000,00", "r-100000"), # R$ e vírgula removidos, ponto preservado como não-separador
        ("Python/Django", "python-django"),
        ("C++ is fun", "c-is-fun"), # ++ removidos
        ("a.b.c", "abc"), # Pontos removidos

        # Casos que testam a ordem das regras (minúsculas, separadores, filtrar, colapsar, aparar)
        ("  TESTE DE SLUG  ", "teste-de-slug"),
        ("  TESTE_DE_SLUG  ", "teste-de-slug"),
        ("  TESTE---DE---SLUG  ", "teste-de-slug"),
        ("  TESTE _ DE - SLUG  ", "teste-de-slug"),
    ]
)
def test_slugify_typical_cases(input_text, expected_slug):
    assert slugify(input_text) == expected_slug

# Testes de casos de borda (valores-limite)
@pytest.mark.parametrize(
    "input_text, expected_slug",
    [
        # String vazia
        ("", ""),

        # Um único caractere
        ("a", "a"),
        ("A", "a"),
        ("1", "1"),
        ("-", ""), # Apenas hífen, deve ser aparado
        (" ", ""), # Apenas espaço, vira hífen e aparado
        ("_", ""), # Apenas underscore, vira hífen e aparado
        (".", ""), # Apenas ponto, filtrado
        ("!", ""), # Apenas símbolo, filtrado

        # Strings com apenas separadores ou símbolos
        ("   ", ""),
        ("___", ""),
        ("---", ""),
        (" - _ ", ""),
        ("!@#", ""),
        (" . , ; ", ""),

        # Strings que começam/terminam com separadores ou símbolos
        ("-foo", "foo"),
        ("foo-", "foo"),
        ("_foo", "foo"),
        ("foo_", "foo"),
        (" foo", "foo"),
        ("foo ", "foo"),
        ("!foo!", "foo"),
        (".foo.", "foo"),
        ("---foo---", "foo"),
        ("   foo   ", "foo"),
        ("___foo___", "foo"),

        # Strings com múltiplos hifens consecutivos
        ("a--b", "a-b"),
        ("a---b", "a-b"),
        ("a----b", "a-b"),
        ("a- -b", "a-b"), # Espaço vira hífen, depois colapsa
        ("a_ _b", "a-b"), # Underscore vira hífen, depois colapsa

        # Strings já no formato slug
        ("already-a-slug", "already-a-slug"),
        ("123-abc-xyz", "123-abc-xyz"),
    ]
)
def test_slugify_edge_cases(input_text, expected_slug):
    assert slugify(input_text) == expected_slug

# Testes de casos inválidos/degenerados (que não lançam erro, mas produzem slug vazio)
@pytest.mark.parametrize(
    "input_text, expected_slug",
    [
        ("!!!", ""),
        ("   ", ""),
        ("___", ""),
        ("---", ""),
        ("!@#$%^&*()", ""),
        (" ", ""),
        ("_", ""),
        ("-", ""),
        (" . , ; ", ""),
        ("ß", ""), # Caractere que não se decompõe em ASCII alfanumérico, deve ser removido
        ("你好世界", ""), # Ideogramas, devem ser removidos
        ("👋🌍🚀", ""), # Emojis, devem ser removidos
        ("  - _ ! @ # $ % ^ & * ( ) + = { } [ ] | \\ : ; \" ' < > , . ? / ` ~   ", ""), # Mix de tudo que não é slug
    ]
)
def test_slugify_degenerate_cases(input_text, expected_slug):
    assert slugify(input_text) == expected_slug

# Testes para verificar invariantes (implicitamente cobertos, mas bom ter alguns focados)
def test_slugify_invariants():
    slug = slugify("  Olá, Mundo! 123_ABC-xyz!!!  ")
    assert all(c.isalnum() or c == '-' for c in slug) # Apenas a-z, 0-9, -
    assert not slug.startswith('-')
    assert not slug.endswith('-')
    assert '--' not in slug

    slug_empty = slugify("!@#$%^&*()")
    assert slug_empty == ""
    assert all(c.isalnum() or c == '-' for c in slug_empty)
    assert not slug_empty.startswith('-')
    assert not slug_empty.endswith('-')
    assert '--' not in slug_empty
