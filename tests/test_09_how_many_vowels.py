import pytest
from importlib import import_module

@pytest.mark.parametrize('text,expected', [
    ('hello', 2),
    ('Apple', 2),
    ('AEIOU', 5),
    ('rhythm', 0),
    ('', 0),
    ('Education', 5),
    ('beautiful day', 6),
])
def test_count_vowels(text,expected):
    func = import_module('how_many_vowels').count_vowels
    assert func(text) == expected
