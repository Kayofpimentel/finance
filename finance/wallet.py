from finance.stock import Stock
from functools import reduce


class Wallet:

    def __init__(self, stocks={}, balance=0) -> None:
        self.__stocks = stocks
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    @property
    def all_stocks(self) -> tuple:
        return tuple(self.__stocks.values())

    @property
    def total_shares_value(self) -> int:
        stocks = tuple(self.__stocks.values())
        stock_values = [stock.total_value for stock in stocks]
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
        if self.__stocks.get(stock.name):
            return False
        self.__stocks[stock.name] = stock
        return True

    def remove_stock(self, stock_name=str) -> bool:
        if self.__stocks.get(stock_name):
            self.__stocks.pop(stock_name)
            return True
        return False

    def single_stock(self, stock_name=str) -> Stock:
        return self.__stocks.get(stock_name)

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
