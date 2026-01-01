#pylint: disable=E0401,E0611,W0718
"""Tests for Commodity module"""

from random import randint
from datetime import datetime
import pytest
from burse import Commodity


def com():
    """Creates Commodity object"""
    return Commodity("A", 10, 20)
c1=com()

def test_init():
    """Testing Commodity object initialization"""
    c = com()
    assert c.name == "A"
    assert c.buy_price == 10
    assert c.sell_price == 20
    try:
        c = Commodity("A", 10, 5)
        assert False
    except AttributeError:
        assert True
    except Exception as e:
        assert e is None


def test_repr():
    """Testing Commodity object representation created by repr() and str() methods"""
    c = com()
    assert repr(c) == "<Commodity A: buy=10, sell=20>"
    assert str(c) == """A: \n\tBuy for: 10
\tSell for: 20>"""


def test_change():
    """Testing Commodity price updates"""
    c =com()
    assert c.buy_price == 10
    assert c.sell_price == 20
    c.update(15, 30)
    assert c.buy_price == 15
    assert c.sell_price == 30
    try:
        c.update(30, 15)
        assert False
    except AttributeError:
        assert True
    except Exception as e:
        assert e is None


def test_log():
    """Basic tests for Commodity history logs"""
    c = com()
    assert len(c.history) == 0
    assert c[datetime.now()] is None
    dt1 = datetime.now()
    c.add_log(dt1)
    c.update(15, 30)
    dt2 = datetime.now()
    c.add_log(dt2)
    assert len(c.history) == 2
    assert c[dt1]["buy"] == 10
    assert c[dt1]["sell"] == 20
    assert c[dt2]["buy"] == 15
    assert c[dt2]["sell"] == 30


@pytest.mark.parametrize("i, buy, sell",[(i,randint(0,100),randint(100,200)) for i in range(20)])
def test_log2(i, buy, sell):
    """
    Parametrized tests for Commodity history logs
    :param i: change index
    :param buy: new buy price
    :param sell: new sell price
    """
    assert len(c1.history) == i
    c1.update(buy, sell)
    dt1 = datetime.now()
    c1.add_log(dt1)
    assert len(c1.history) == i + 1
    assert c1[dt1]["buy"] == buy
    assert c1[dt1]["sell"] == sell
    assert c1.buy_price == buy
    assert c1.sell_price == sell


def test_false_log():
    """Test fail after adding log paster than last log"""
    c = com()
    c.add_log(datetime.now())
    try:
        c.add_log(datetime(1,1,1))
        assert False
    except AttributeError:
        assert True
    except Exception as e:
        assert e is None
