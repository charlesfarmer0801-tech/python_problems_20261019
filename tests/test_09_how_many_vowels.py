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
], ids=["lowercase-word","mixed-case-word","uppercase-vowels","no-vowels","empty-string","mixed-case-vowels","sentence-with-space"])
def test_count_vowels(text,expected, verify_output):
    func = import_module('how_many_vowels').count_vowels
    verify_output(func(text), expected)
