import pytest
from importlib import import_module

@pytest.mark.parametrize('price,discount,expected', [
    (1500, 50, 750),
    (89, 20, 71.2),
    (100, 75, 25),
    (35, 0, 35),
    (35, 100, 0),
    (125, 15, 106.25),
], ids=["half-off","twenty-percent-off","seventy-five-percent-off","zero-discount","full-discount","fifteen-percent-off"])
def test_discount(price,discount,expected, verify_output):
    func = import_module('find_the_discount').dis
    verify_output(func(price,discount), expected)
