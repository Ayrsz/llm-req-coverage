import pytest
from solution import most_frequent


def test_empty_list():
    assert most_frequent([]) == ""


def test_single_element_list():
    assert most_frequent(["a"]) == "a"
    assert most_frequent(["hello"]) == "hello"


def test_clear_winner():
    assert most_frequent(["a", "b", "a"]) == "a"
    assert most_frequent(["apple", "banana", "apple", "orange", "apple"]) == "apple"
    assert most_frequent(["x", "y", "z", "x", "y", "x"]) == "x"


def test_all_distinct_elements_first_wins():
    assert most_frequent(["c", "b", "a"]) == "c"
    assert most_frequent(["apple", "banana", "orange"]) == "apple"


def test_tie_breaker_two_elements_first_wins():
    assert most_frequent(["a", "b"]) == "a"
    assert most_frequent(["hello", "world"]) == "hello"


def test_tie_breaker_multiple_occurrences():
    assert most_frequent(["b", "a", "a", "b"]) == "b"
    assert most_frequent(["x", "y", "x", "y"]) == "x"
    assert most_frequent(["y", "x", "y", "x"]) == "y"
    assert most_frequent(["apple", "banana", "apple", "banana", "cherry"]) == "apple"
    assert most_frequent(["banana", "apple", "banana", "apple", "cherry"]) == "banana"


def test_complex_scenarios():
    assert most_frequent(["a", "b", "c", "a", "b"]) == "a"
    assert most_frequent(["b", "a", "c", "b", "a"]) == "b"
    assert most_frequent(["c", "a", "b", "c", "a", "b"]) == "c"
    assert most_frequent(["a", "b", "c", "d"]) == "a"
    assert most_frequent(["long_string", "short", "long_string", "medium"]) == "long_string"
    assert most_frequent(["1", "2", "1", "3", "2", "1"]) == "1"


def test_strings_with_empty_or_special_chars():
    assert most_frequent(["", "a", "", "b"]) == ""
    assert most_frequent([" ", "a", " ", "b"]) == " "
    assert most_frequent(["!", "@", "!", "#"]) == "!"


def test_case_sensitivity():
    assert most_frequent(["apple", "Apple", "apple"]) == "apple"
    assert most_frequent(["Apple", "apple", "Apple"]) == "Apple"
    assert most_frequent(["a", "A", "b", "B"]) == "a"
