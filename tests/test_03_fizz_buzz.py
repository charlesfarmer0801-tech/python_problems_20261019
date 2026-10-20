import pytest
from importlib import import_module

@pytest.mark.parametrize('number,expected', [
    (3, 'Fizz'), (5, 'Buzz'), (15, 'FizzBuzz'),
    (30, 'FizzBuzz'), (9, 'Fizz'), (10, 'Buzz'),
    (7, '7'), (22, '22'), (1, '1'),
])
def test_fizz_buzz(number,expected):
    func = import_module('fizz_buzz').fizz_buzz
    assert func(number) == expected
