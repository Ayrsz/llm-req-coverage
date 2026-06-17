import pytest
from solution import filter_by_tag

BASE_BOOKMARKS = [
    {"title": "Python docs", "tags": ["dev", "python"]},
    {"title": "Receitas",    "tags": ["casa", "comida"]},
    {"title": "Flask",       "tags": ["dev", "Python"]},
    {"title": "Django",      "tags": ["web", "python", "framework"]},
    {"title": "Empty Tags",  "tags": []},
    {"title": "Only One Tag", "tags": ["single"]},
    {"title": "Another Dev", "tags": ["DEV", "backend"]},
    {"title": "Frontend",    "tags": ["web", "javascript"]},
    {"title": "Case Test",   "tags": ["CaSeInSeNsItIvE"]},
    {"title": "Numeric Tag", "tags": ["123tag"]},
]

@pytest.mark.parametrize(
    "bookmarks, tag, expected",
    [
        # AC1: Caso típico, múltiplos matches, ordem preservada
        (BASE_BOOKMARKS, "dev", ["Python docs", "Flask", "Another Dev"]),
        # AC2: Correspondência case-insensitive
        (BASE_BOOKMARKS, "python", ["Python docs", "Flask", "Django"]),
        (BASE_BOOKMARKS, "PYTHON", ["Python docs", "Flask", "Django"]),
        (BASE_BOOKMARKS, "CaSeInSeNsItIvE", ["Case Test"]),
        (BASE_BOOKMARKS, "caseinsensitive", ["Case Test"]),
        # AC3: Correspondência exata, não substring
        (BASE_BOOKMARKS, "py", []),
        (BASE_BOOKMARKS, "tag", []), # "tag" não casa com "123tag"
        # AC4: Tag vazia
        (BASE_BOOKMARKS, "", []),
        # AC5: Lista de bookmarks vazia
        ([], "dev", []),
        # AC6: Um único match
        (BASE_BOOKMARKS, "comida", ["Receitas"]),
        # Tag não encontrada em nenhum bookmark
        (BASE_BOOKMARKS, "nonexistent", []),
        # Bookmark com lista de tags vazia (não deve casar)
        (BASE_BOOKMARKS, "empty", []), # "empty" não é uma tag do bookmark "Empty Tags"
        # Tag presente em bookmark com múltiplas tags
        (BASE_BOOKMARKS, "framework", ["Django"]),
        # Tag presente em bookmark com apenas uma tag
        (BASE_BOOKMARKS, "single", ["Only One Tag"]),
        # Todos os bookmarks casam
        ([{"title": "A", "tags": ["common"]}, {"title": "B", "tags": ["common"]}], "common", ["A", "B"]),
        # Tag com números
        (BASE_BOOKMARKS, "123tag", ["Numeric Tag"]),
        (BASE_BOOKMARKS, "123TAG", ["Numeric Tag"]), # Case-insensitive para tags numéricas
        # Tag que é substring de outra tag, mas não exata
        ([{"title": "Full", "tags": ["fulltag"]}], "full", []),
    ]
)
def test_filter_by_tag_various_scenarios(bookmarks, tag, expected):
    assert filter_by_tag(bookmarks, tag) == expected

def test_filter_by_tag_no_matching_bookmarks_specific():
    # Tag existe, mas não nos bookmarks fornecidos
    bms = [
        {"title": "Python docs", "tags": ["dev"]},
        {"title": "Receitas",    "tags": ["casa"]},
    ]
    assert filter_by_tag(bms, "python") == []

def test_filter_by_tag_bookmark_with_empty_tags_list_specific():
    # Um bookmark tem uma lista de tags vazia, nunca deve casar
    bms = [
        {"title": "No Tags", "tags": []},
        {"title": "Has Tag", "tags": ["test"]},
    ]
    assert filter_by_tag(bms, "test") == ["Has Tag"]
    assert filter_by_tag(bms, "No Tags") == [] # Não deve casar o título como tag

def test_filter_by_tag_order_preservation_complex():
    # Garante que a ordem é estritamente preservada mesmo com matches mistos
    bms = [
        {"title": "First", "tags": ["a"]},
        {"title": "Second", "tags": ["b"]},
        {"title": "Third", "tags": ["a"]},
        {"title": "Fourth", "tags": ["c"]},
        {"title": "Fifth", "tags": ["a"]},
    ]
    assert filter_by_tag(bms, "a") == ["First", "Third", "Fifth"]
    assert filter_by_tag(bms, "b") == ["Second"]
    assert filter_by_tag(bms, "c") == ["Fourth"]

def test_filter_by_tag_all_bookmarks_match_specific():
    bms = [
        {"title": "Book1", "tags": ["common", "tag1"]},
        {"title": "Book2", "tags": ["common", "tag2"]},
        {"title": "Book3", "tags": ["common"]},
    ]
    assert filter_by_tag(bms, "common") == ["Book1", "Book2", "Book3"]

def test_filter_by_tag_no_bookmarks_match_specific():
    bms = [
        {"title": "Book1", "tags": ["tag1"]},
        {"title": "Book2", "tags": ["tag2"]},
    ]
    assert filter_by_tag(bms, "nonexistent") == []

def test_filter_by_tag_case_insensitive_with_mixed_case_tags():
    bms = [
        {"title": "Doc 1", "tags": ["Python"]},
        {"title": "Doc 2", "tags": ["python"]},
        {"title": "Doc 3", "tags": ["PYTHON"]},
    ]
    assert filter_by_tag(bms, "python") == ["Doc 1", "Doc 2", "Doc 3"]
    assert filter_by_tag(bms, "PYTHON") == ["Doc 1", "Doc 2", "Doc 3"]
    assert filter_by_tag(bms, "PyThOn") == ["Doc 1", "Doc 2", "Doc 3"]
