class Stock:

    def __init__(self, name='', shares=0, value=0) -> None:
        self.__value = value
        self.__shares = shares
        self.__name = name

    @property
    def value(self) -> int:
        return self.__value

    @property
    def total_value(self) -> int:
        return self.__value * self.__shares

    @property
    def shares(self) -> int:
        return self.__shares

    @shares.setter
    def shares(self, shares):
        self.__shares = shares

    @property
    def name(self) -> str:
        return self.__name
