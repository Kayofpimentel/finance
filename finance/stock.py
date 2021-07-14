class Stock:

    def __init__(self, name='', share=0, value=0) -> None:
        self.__value = value
        self.__share = share
        self.__name = name

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    @property
    def total_value(self) -> int:
        return self.__value * self.__share

    @property
    def share(self) -> int:
        return self.__share

    @share.setter
    def shares(self, new_share):
        self.__share = new_share

    @property
    def name(self) -> str:
        return self.__name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, o: object) -> bool:
        return self.__hash__ == o.__hash__
