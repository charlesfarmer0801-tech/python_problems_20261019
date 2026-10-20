import pytest
from importlib import import_module

# Per Edabit use pi = 3.14 for the circle circumference.
@pytest.mark.parametrize('radius,square_area,expected', [
    (1, 1, True),
    (1, 4, False),
    (2, 9, True),
    (1, 3, False),
    (0, 9, False),
    (3, 16, True),
], ids=["circle-larger","square-larger","circle-larger-case-two","square-larger-case-two","zero-radius","circle-larger-case-three"])
def test_circle_or_square(radius,square_area,expected, verify_output):
    func = import_module('circle_or_square').circle_or_square
    verify_output(func(radius,square_area), expected)
