import pytest
from importlib import import_module

@pytest.mark.parametrize('damage,speed,time,expected', [
    (40, 5, 'second', 200),
    (100, 1, 'minute', 6000),
    (2, 100, 'hour', 720000),
    (20, 0.5, 'minute', 600),
    (2, 400, 'hour', 2880000),
    (-23, 20, 'second', 'invalid'),
    (20, -2, 'hour', 'invalid'),
    (0, 10, 'minute', 0),
], ids=["per-second","per-minute","per-hour","fractional-speed","large-hourly-damage","negative-damage","negative-speed","zero-damage"])
def test_damage(damage,speed,time,expected, verify_output):
    func = import_module('calc_damage').damage
    verify_output(func(damage,speed,time), expected)
