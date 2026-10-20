import pytest
from importlib import import_module

@pytest.mark.parametrize('n1,n2,expected', [
    ('2', '3', '5'),
    ('10', '-2', '8'),
    (7, 9, '16'),
    (-3, -11, '-14'),
    ('0', '0', '0'),
    ('', '7', 'Invalid Operation'),
    (None, '5', 'Invalid Operation'),
    ('2', None, 'Invalid Operation'),
], ids=["positive-numbers","positive-and-negative","integer-inputs","two-negative-numbers","adding-zero","empty-first-input","none-first-input","none-second-input"])
def test_add(n1, n2, expected, verify_output):
    add = import_module('adding_numbers').add
    verify_output(add(n1, n2), expected)
