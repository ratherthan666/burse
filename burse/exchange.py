#pylint: disable=C0301,R0903
"""Module for class representing Exchange"""

import random
import time

from .commodity import Commodity


class Exchange:
    """
    Class that simulates exchange
    """

    class Trade:
        """Represents a trade"""

        def __init__(self, commodity: str, trade_buy: bool, amount: int):
            """
            Initialize the trade
            :param commodity: name of the commodity in trade
            :param trade_buy: indicates if the trade is a buy or sell
            :param amount: amount of goods in trade
            """
            self.commodity = commodity
            self.trade_buy = trade_buy
            self.amount = amount


    _MIN_SPREAD = 0.001
    _MAX_CHANGE = 0.005
    _SENSITIVITY = 0.001

    def __init__(self):
        """
        Initialize the exchange with no _commodities registered.
        """
        self._commodities: dict[str, Commodity] = {}
        self._trades_to_process: list[Exchange.Trade] = []

    def __getitem__(self, commodity_name: str) -> Commodity:
        """
        Simplifier for getting commodity object
        :param commodity_name: commodity name to extract
        """
        return self._commodities[commodity_name]

    def __repr__(self):
        st =  f"<Exchange commodities: {len(self._commodities)}, unprocessed_trades: {len(self._trades_to_process)}>"
        for c in self._commodities.values():
            st += f"\n\t{c.__repr__()}"
        return st

    def __iter__(self):
        """
        Iterate over the exchange _commodities
        :return: actual iteration
        """
        for k, c in self._commodities.items():
            yield k, c

    @property
    def current_prices(self) -> dict[str,tuple[float,float]]:
        """
        Returns the current prices of the _commodities
        :return: dictionary of current price represented as tuples (buy price, sell price)
        """
        return {c.name: (c.buy_price, c.sell_price) for c in self._commodities.values()}

    @property
    def commodity_names(self) -> list[str]:
        """
        Returns a list of all _commodities registered
        :return: list of _commodities
        """
        return list(self._commodities.keys())

    def add_commodity(self, commodity: Commodity):
        """
        Adds a commodity to the exchange
        :param commodity: commodity to add to exchange
        :raises ValueError: if commodity is already registered
        """
        if commodity.name in self._commodities:
            raise ValueError("Commodity already exists")
        self._commodities[commodity.name] = commodity

    def _control_and_update_prices(self, commodity_name: str, new_buy: float, new_sell: float):
        """Controls some rules (prices bigger than 0, buy < sell) and updates prices"""

        new_buy = max(new_buy, self._MIN_SPREAD)

        if new_sell <= new_buy:
            new_sell = new_buy * (1 + self._MIN_SPREAD)

        self._commodities[commodity_name].update(new_buy, new_sell)
        self._commodities[commodity_name].add_log(time.time())

    def _random_price_movement(self, commodity_name: str) -> None:
        """
        Function that generates a fully random price movement
        :param commodity_name: name of the commodity
        """
        delta_buy = 1 + random.uniform(-self._MAX_CHANGE, self._MAX_CHANGE)
        delta_sell = 1 + random.uniform(-self._MAX_CHANGE, self._MAX_CHANGE)

        new_buy = self._commodities[commodity_name].buy_price * delta_buy
        new_sell = self._commodities[commodity_name].sell_price * delta_sell

        self._control_and_update_prices(commodity_name, new_buy, new_sell)

    @staticmethod
    def _random_trades(commodity_name: str, min_trades: int = 1, max_trades: int = 5, max_amount: int = 20) -> list[Trade]:
        if min_trades > max_trades or min_trades <= 0:
            raise ValueError("min_trades must be greater than or equal to 0")
        if max_amount <= 0:
            raise ValueError("max_amount must be greater than or equal to 0")

        trades = []
        for _ in range(random.randint(min_trades, max_trades)):
            trades.append(Exchange.Trade(commodity_name, random.choice([True, False]), random.randint(1, max_amount)))
        return trades

    def _generate_random_trades(self):
        """
        Generate random trades and add them to the list of unprocessed trades
        """
        for c in self.commodity_names:
            self._trades_to_process.extend(Exchange._random_trades(c))

    def process_trades(self):
        """
        Processes all unprocessed trades
        """
        processing = self._trades_to_process.copy()
        self._trades_to_process.clear()
        for n, c in self._commodities.items():
            total_buy = sum(t.amount for t in processing if t.trade_buy and t.commodity == n)
            total_sell = sum(t.amount for t in processing if not t.trade_buy and t.commodity == n)

            imbalance = total_sell - total_buy
            delta = imbalance * self._SENSITIVITY

            new_buy = c.buy_price + delta
            new_sell = c.sell_price + delta

            self._control_and_update_prices(n, new_buy, new_sell)

    def random_price_movement_all(self) -> None:
        """
        Runs random price movement for all _commodities
        """
        for commodity in self._commodities:
            self._random_price_movement(commodity)
        self._generate_random_trades()
        self.process_trades()

    def add_trade(self, commodity: str, trade_buy: bool, amount: int) -> float:
        """
        Add manually created trade to trades list
        :param commodity: commodity to trade with
        :param trade_buy: indicates if the trade is a buy or sell
        :param amount: amount of goods in trade
        :return: money spent on this trade
        """
        self._trades_to_process.append(Exchange.Trade(commodity, trade_buy, amount))
        return amount * (self._commodities[commodity].buy_price if trade_buy else self._commodities[commodity].sell_price)
