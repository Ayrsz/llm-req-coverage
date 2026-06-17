from solution import filter_by_tag

def test_tag_present_exact_case_sensitive():
    bookmarks = [
        {"title": "Python docs", "tags": ["dev", "python"]},
        {"title": "Receitas",    "tags": ["casa", "comida"]},
        {"title": "Flask",       "tags": ["dev", "Python"]},
    ]
    tag = "dev"
    expected = ["Python docs", "Flask"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_tag_present_case_insensitive():
    bookmarks = [
        {"title": "Python docs", "tags": ["dev", "python"]},
        {"title": "Receitas",    "tags": ["casa", "comida"]},
        {"title": "Flask",       "tags": ["dev", "Python"]},
    ]
    tag = "python"
    expected = ["Python docs", "Flask"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_tag_substring_should_not_match():
    bookmarks = [
        {"title": "Python docs", "tags": ["dev", "python"]},
        {"title": "Receitas",    "tags": ["casa", "comida"]},
        {"title": "Flask",       "tags": ["dev", "Python"]},
    ]
    tag = "py"
    expected = []
    assert filter_by_tag(bookmarks, tag) == expected

def test_no_matching_bookmarks():
    bookmarks = [
        {"title": "Python docs", "tags": ["dev", "python"]},
        {"title": "Receitas",    "tags": ["casa", "comida"]},
        {"title": "Flask",       "tags": ["dev", "Python"]},
    ]
    tag = "javascript"
    expected = []
    assert filter_by_tag(bookmarks, tag) == expected

def test_all_bookmarks_match():
    bookmarks = [
        {"title": "Doc 1", "tags": ["common_tag", "other"]},
        {"title": "Doc 2", "tags": ["common_tag"]},
        {"title": "Doc 3", "tags": ["another", "common_tag"]},
    ]
    tag = "common_tag"
    expected = ["Doc 1", "Doc 2", "Doc 3"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_original_order_preserved():
    bookmarks = [
        {"title": "First", "tags": ["a"]},
        {"title": "Second", "tags": ["b"]},
        {"title": "Third", "tags": ["a"]},
        {"title": "Fourth", "tags": ["c"]},
        {"title": "Fifth", "tags": ["a"]},
    ]
    tag = "a"
    expected = ["First", "Third", "Fifth"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_tag_present_in_single_bookmark():
    bookmarks = [
        {"title": "Python docs", "tags": ["dev", "python"]},
        {"title": "Receitas",    "tags": ["casa", "comida"]},
        {"title": "Flask",       "tags": ["dev", "Python"]},
    ]
    tag = "comida"
    expected = ["Receitas"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_empty_tag():
    bookmarks = [
        {"title": "Python docs", "tags": ["dev", "python"]},
        {"title": "Receitas",    "tags": ["casa", "comida"]},
    ]
    tag = ""
    expected = []
    assert filter_by_tag(bookmarks, tag) == expected

def test_empty_bookmarks_list():
    bookmarks = []
    tag = "dev"
    expected = []
    assert filter_by_tag(bookmarks, tag) == expected

def test_bookmark_with_empty_tags_list():
    bookmarks = [
        {"title": "Bookmark sem tags", "tags": []},
        {"title": "Outro bookmark", "tags": ["tag1"]},
    ]
    tag = "tag1"
    expected = ["Outro bookmark"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_single_character_tag():
    bookmarks = [
        {"title": "A book", "tags": ["a", "b"]},
        {"title": "B book", "tags": ["b"]},
    ]
    tag = "a"
    expected = ["A book"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_long_tag():
    bookmarks = [
        {"title": "Long Tag Book", "tags": ["thisisareallylongtagthatshouldwork"]},
        {"title": "Short Tag Book", "tags": ["short"]},
    ]
    tag = "thisisareallylongtagthatshouldwork"
    expected = ["Long Tag Book"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_empty_tag_reinforcement():
    bookmarks = [
        {"title": "Python docs", "tags": ["dev", "python"]},
    ]
    tag = ""
    expected = []
    assert filter_by_tag(bookmarks, tag) == expected

def test_bookmark_with_empty_tags_list_no_match():
    bookmarks = [
        {"title": "Bookmark sem tags", "tags": []},
        {"title": "Outro bookmark", "tags": ["tag1"]},
    ]
    tag = "tag2"
    expected = []
    assert filter_by_tag(bookmarks, tag) == expected

def test_tag_with_special_chars_exact():
    bookmarks = [
        {"title": "Special Chars", "tags": ["tag-with-hyphen", "tag_with_underscore", "tag with space"]},
        {"title": "Normal", "tags": ["normal"]},
    ]
    tag = "tag-with-hyphen"
    expected = ["Special Chars"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_tag_with_special_chars_case_insensitive():
    bookmarks = [
        {"title": "Special Chars", "tags": ["Tag-With-Hyphen"]},
    ]
    tag = "tag-with-hyphen"
    expected = ["Special Chars"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_bookmark_with_duplicate_tags_in_list():
    bookmarks = [
        {"title": "Duplicate Tags", "tags": ["dev", "python", "dev"]},
    ]
    tag = "dev"
    expected = ["Duplicate Tags"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_duplicate_bookmarks_in_input_list():
    bookmarks = [
        {"title": "Python docs", "tags": ["dev", "python"]},
        {"title": "Receitas",    "tags": ["casa", "comida"]},
        {"title": "Python docs", "tags": ["dev", "python"]}, # Duplicado
    ]
    tag = "dev"
    expected = ["Python docs", "Python docs"]
    assert filter_by_tag(bookmarks, tag) == expected

def test_invariants_no_match_length():
    bookmarks = [
        {"title": "Python docs", "tags": ["dev", "python"]},
        {"title": "Receitas",    "tags": ["casa", "comida"]},
    ]
    tag = "nonexistent"
    result = filter_by_tag(bookmarks, tag)
    assert result == []
    assert len(result) <= len(bookmarks)

def test_invariants_full_match_length():
    bookmarks = [
        {"title": "Python docs", "tags": ["dev", "python"]},
        {"title": "Receitas",    "tags": ["dev", "comida"]},
    ]
    tag = "dev"
    result = filter_by_tag(bookmarks, tag)
    assert result == ["Python docs", "Receitas"]
    assert len(result) <= len(bookmarks)
