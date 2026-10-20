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
])
def test_circle_or_square(radius,square_area,expected):
    func = import_module('circle_or_square').circle_or_square
    assert func(radius,square_area) is expected
