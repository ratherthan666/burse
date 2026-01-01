import pytest
from random import randint
from burse import Exchange
from burse import Commodity

ex = Exchange()

@pytest.mark.parametrize("i,name,init_buy_price,init_sell_price", [
    (i,f"{i}",randint(0,100),randint(100,200)) for i in range(20)
])
def test_correct_load_commodities(i, name, init_buy_price, init_sell_price):
    c = Commodity(name, init_buy_price, init_sell_price)
    ex.add_commodity(c)

    assert len(ex.commodity_names) == i+1
    assert ex.commodity_names[i] == name
    assert ex[name] is c

@pytest.mark.parametrize("name,init_buy_price,init_sell_price", [
    (f"{i}",randint(101,200),randint(0,100)) for i in range(20)
])
def test_incorrect_load_commodities(name, init_buy_price, init_sell_price):
    try:
        c = Commodity(name, init_buy_price, init_sell_price)
        ex.add_commodity(c)
        assert False
    except AttributeError:
        pass
