import pytest
from importlib import import_module

@pytest.mark.parametrize('number,length,expected', [
    (7, 5, [7,14,21,28,35]),
    (12, 10, [12,24,36,48,60,72,84,96,108,120]),
    (17, 6, [17,34,51,68,85,102]),
    (3, 1, [3]),
    (4, 4, [4,8,12,16]),
    (1, 7, [1,2,3,4,5,6,7]),
])
def test_list_of_multiples(number,length,expected):
    func = import_module('list_of_multiples').list_of_multiples
    assert func(number,length) == expected
