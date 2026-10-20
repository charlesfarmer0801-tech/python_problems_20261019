import pytest
from importlib import import_module

@pytest.mark.parametrize('details,expected', [
    ({'cost_price': 32.67, 'sell_price': 45.0, 'inventory': 120}, 1480),
    ({'cost_price': 0.0, 'sell_price': 25.0, 'inventory': 4}, 100),
    ({'cost_price': 20.0, 'sell_price': 15.0, 'inventory': 3}, -15),
    ({'cost_price': 1.0, 'sell_price': 1.0, 'inventory': 100}, 0),
    ({'cost_price': 5.75, 'sell_price': 6.25, 'inventory': 10}, 5),
], ids=["standard-profit","zero-cost","negative-profit","break-even","fractional-profit"])
def test_profit(details,expected, verify_output):
    func = import_module('calc_the_profit').profit
    verify_output(func(details), expected)
