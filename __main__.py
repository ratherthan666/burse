#pylint: disable=E0401,E0611
"""Main server module"""

from burse import Exchange
from burse import Commodity
from multi_burse import server_loop


def _load_commodities(ex):
    with open("config/commodities.csv", "r", encoding="utf8") as f:
        for line in f.readlines():
            name, buy, sell = line[:-1].split(",")
            ex.add_commodity(Commodity(name, float(buy), float(sell)))

if __name__ == "__main__":
    exchange = Exchange()
    _load_commodities(exchange)
    server_loop("127.0.0.1", 12345, exchange)
