#pylint: disable=E0401,E0611,W0718
"""Tests for Exchange module"""

from random import randint
import pytest
from burse import Exchange
from burse import Commodity

ex = Exchange()

@pytest.mark.parametrize("i,name,init_buy_price,init_sell_price", [
    (i,f"{i}",randint(0,100),randint(100,200)) for i in range(20)
])
def test_correct_load_commodities(i, name, init_buy_price, init_sell_price):
    """
    Tests correctly created commodities loaded into Exchange
    :param i: commodity index
    :param name: commodity name
    :param init_buy_price: initial buy price
    :param init_sell_price: initial sell price
    """
    c = Commodity(name, init_buy_price, init_sell_price)
    ex.add_commodity(c)

    assert len(ex.commodity_names) == i+1
    assert ex.commodity_names[i] == name
    assert ex[name] is c

@pytest.mark.parametrize("name,init_buy_price,init_sell_price", [
    (f"{i}",randint(101,200),randint(0,100)) for i in range(20)
])
def test_incorrect_load_commodities(name, init_buy_price, init_sell_price):
    """
    Tests incorrectly created commodities loaded into Exchange
    :param name: commodity name
    :param init_buy_price: initial buy price
    :param init_sell_price: initial sell price
    """
    try:
        c = Commodity(name, init_buy_price, init_sell_price)
        ex.add_commodity(c)
        assert False
    except AttributeError:
        pass
