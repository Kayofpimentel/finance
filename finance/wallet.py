from finance.stock import Stock
from functools import reduce


class Wallet:

    def __init__(self, name=str, stocks=set, balance=int) -> None:
        self.__name = name
        self.__stocks = stocks
        self.__balance = balance

    @property
    def name(self):
        return self.__name

    @property
    def balance(self):
        return self.__balance

    @property
    def stocks(self) -> set:
        return self.__stocks

    @property
    def total_shares_value(self) -> int:
        stock_values = [stock.total_value for stock in self.__stocks]
        total_value = reduce(
            lambda total_value, stock_value: total_value + stock_value, stock_values, 0)
        return total_value

    def add_balance(self, value) -> bool:
        if not isinstance(value, int):
            return False
        elif value <= 0:
            return False
        self.__balance += value
        return True

    def remove_balance(self, value) -> bool:
        if not isinstance(value, int):
            return False
        elif value <= 0 or abs(value) > self.balance:
            return False
        self.__balance -= value
        return True

    def add_stock(self, stock=Stock) -> bool:
        if stock in self.__stocks:
            return False
        self.__stocks.add(stock)
        return True

    def remove_stock(self, stock_name=str) -> bool:
        for stock in self.stocks:
            if stock.name == stock_name:
                self.__stocks.remove(stock)
                return True
        return False

    def single_stock(self, stock_name=str) -> Stock:
        for stock in self.stocks:
            if stock.name == stock_name:
                return stock
        return None

    def stock_shares_value(self, stock_name):
        stock = self.single_stock(stock_name)
        if not stock:
            return False
        return stock.shares * stock.value

    def add_stock_share(self, stock_name, shares):
        stock = self.single_stock(stock_name)
        if not (isinstance(shares, int) and stock):
            return False
        elif shares <= 0:
            return False
        stock.shares += shares
        return True

    def remove_stock_share(self, stock_name, shares):
        stock = self.single_stock(stock_name)
        if not (isinstance(shares, int) and stock):
            return False
        elif shares <= 0 or abs(shares) > stock.shares:
            return False
        stock.shares -= shares
        return True

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, o: object) -> bool:
        return self.__hash__ == o.__hash__
