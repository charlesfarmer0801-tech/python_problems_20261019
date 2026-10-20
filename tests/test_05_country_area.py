import pytest
from importlib import import_module

# Edabit's stated world landmass constant is 148,940,000 sq km.
@pytest.mark.parametrize('country,area', [
    ('Russia', 17_098_242),
    ('USA', 9_833_517),
    ('Australia', 7_692_024),
    ('Narnia', 0),
    ('World', 148_940_000),
    ('Japan', 377_975),
])
def test_area_of_country(country,area):
    func = import_module('country_area').area_of_country
    percentage = round(area / 148_940_000 * 100, 2)
    expected = f"{country} is {percentage}% of the total world's landmass"
    assert func(country,area) == expected
