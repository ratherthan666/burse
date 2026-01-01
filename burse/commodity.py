"""Module for class representing single commodity"""

class Commodity:
    """
    Represents an individual commodity with its prices for selling/buying
    """

    def __init__(self, name: str, init_buy_price: float, init_sell_price: float) -> None:
        """
        Initializes a new commodity
        :param name: name of the commodity
        :param init_buy_price: initial buy price
        :param init_sell_price: initial sell price
        """
        if init_buy_price > init_sell_price:
            raise AttributeError("Initial buy price is higher than initial sell price")
        self.name = name
        self.buy_price = init_buy_price
        self.sell_price = init_sell_price
        self.history = []

    def update(self, buy_price: float, sell_price: float) -> None:
        """
        Updates the buy and sell prices of the commodity
        :param buy_price: new buy price
        :param sell_price: new sell price
        """
        self.buy_price = buy_price
        self.sell_price = sell_price

    def add_log(self, time) -> None:
        """
        Add a log to commodity history
        :param time: time for log
        :return:
        """
        if len(self.history) != 0 and time <= self.history[-1]["time"]:
            raise AttributeError("Time is paster than previous log")
        self.history.append({
            "time": time,
            "buy": self.buy_price,
            "sell": self.sell_price,
        })

    def __repr__(self) -> str:
        """
        :return: string representation of commodity
        """
        return f"<Commodity {self.name}: buy={self.buy_price}, sell={self.sell_price}>"

    def __str__(self) -> str:
        """
        :return: string description for commodity
        """
        return f"{self.name}: \n\tBuy for {self.buy_price}\n\tSell for: {self.sell_price}>"

    def __getitem__(self, time) -> dict|None:
        """
        Return log for given time if exists
        :param time: time to find log of
        :return: founded time
        """
        for log in self.history:
            if log["time"] == time:
                return log
        return None
