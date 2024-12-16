from src.hand import Hands


class User:
    def __init__(self, name: str, coin: int, betcoin: int):
        self.__name = name
        self.coin = coin
        self.betcoin = betcoin
        self.__hands = Hands()

    @property
    def name(self):
        return self.__name
    
    @property
    def hands(self):
        return self.__hands