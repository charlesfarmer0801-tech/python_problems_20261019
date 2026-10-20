import pytest
from importlib import import_module

@pytest.mark.parametrize('num1,operator,num2,expected', [
    (2, '+', 3, 5),
    (12, '-', 9, 3),
    (4, '*', 8, 32),
    (18, '/', 6, 3),
    (-5, '+', 7, 2),
    (4, '-', 11, -7),
    (2.5, '*', 4, 10),
    (3, '/', 2, 1.5),
    (9, '/', 0, "Can't divide by 0!"),
])
def test_calculator(num1,operator,num2,expected):
    func = import_module('basic_calculator').calculator
    assert func(num1,operator,num2) == expected
