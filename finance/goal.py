class Goal:

    def __init__(self, name=str, stocks=set, apportion=int) -> None:
        self.__name = name
        self.__stocks = stocks
        self.__apportion = apportion

    @property
    def name(self):
        return self.__name

    @property
    def stocks(self):
        return self.__stocks

    @property
    def apportion(self):
        return self.__apportion

    @apportion.setter
    def apportion(self, new_apportion):
        self.__apportion = new_apportion

    def single_stock(self, stock_name):
        for stock in self.stocks:
            if stock.name == stock_name:
                return stock
        return None

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, o: object) -> bool:
        return self.__hash__ == o.__hash__
