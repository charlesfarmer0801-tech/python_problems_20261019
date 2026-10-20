import pytest
from importlib import import_module

@pytest.mark.parametrize('number,expected', [
    (3, 'Fizz'), (5, 'Buzz'), (15, 'FizzBuzz'),
    (30, 'FizzBuzz'), (9, 'Fizz'), (10, 'Buzz'),
    (7, '7'), (22, '22'), (1, '1'),
], ids=["divisible-by-three","divisible-by-five","divisible-by-both","thirty-divisible-by-both","nine-divisible-by-three","ten-divisible-by-five","not-divisible-seven","not-divisible-twenty-two","not-divisible-one"])
def test_fizz_buzz(number,expected, verify_output):
    func = import_module('fizz_buzz').fizz_buzz
    verify_output(func(number), expected)
