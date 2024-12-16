import numpy as np

from src.card import Deck
from src.hand import Hands
from src.user import User

class BlackJack:
    def __init__(self):
        self.__users = [User(f"プレイヤー{i+1}", 100, 10) for i in range(3)]
        self.__dealer_hands = Hands()
        self.__deck = Deck()
        self.__round = 1

    def add_round(self):
        self.__round += 1

    def bet(self, user_index: int, add_betcoin: int):
        user = self.__users[user_index]
        if (user.betcoin + add_betcoin) < 10:
            add_betcoin = 10 - user.betcoin
        if (user.coin - add_betcoin) < 0:
            add_betcoin = user.coin
        user.betcoin += add_betcoin
        user.coin -= add_betcoin
    
    def start(self):
        for user in self.__users:
            user.hands.clear_hands()
        self.__dealer_hands.clear_hands()
        self.__deck.reset_card()
        for hand in [user.hands for user in self.__users] + [self.__dealer_hands]:
            hand.add_hands(self.__deck.draw_card())

    def hit(self, user_index: int) -> bool:
        self.__users[user_index].hands.add_hands(self.__deck.draw_card())
        if self.__users[user_index].hands.hand_strength < 21:
            return False
        return True

    def dealer(self):
        while self.__dealer_hands.hand_strength < 17:
            self.__dealer_hands.add_hands(self.__deck.draw_card())

    def renew_coin(self, victory_or_defeat):
        if len(victory_or_defeat) != 3:
            raise ValueError("victory_or_defeat must have exactly 3 elements")
        for i in range(3):
            user = self.__users[i]
            user.coin += user.betcoin * victory_or_defeat[i]
            user.betcoin = 10


    def ranking(self):
        user_list = []
        for i in range(3):
            user = self.__users[i]
            user_list.append([user.name, user.coin])
        user_list.sort(key=lambda x: x[1], reverse=True)
        return user_list
        
    def judge(self):
        dealer_strength = self.__dealer_hands.hand_strength
        user_strength = [self.__users[i].hands.hand_strength for i in range(3)]

        victory_or_defeat = [0,0,0]

        for i in range(3):
            if user_strength[i] > 21:
                victory_or_defeat[i] = 0
            elif dealer_strength > 21:
                victory_or_defeat[i] = 2
            elif user_strength[i] > dealer_strength:
                victory_or_defeat[i] = 2
            elif user_strength[i] == dealer_strength:
                victory_or_defeat[i] = 0
            else:
                victory_or_defeat[i] = 0

        self.renew_coin(victory_or_defeat)
        

    def clear_result(self):
        for i in range(3):
            self.__users[i].coin = 100
            self.__users[i].betcoin = 10
            self.__users[i].hands.clear_hands()
        self.__dealer_hands.clear_hands()
        self.__deck.reset_card()
        self.__round = 1


    @property
    def user_coins(self) -> list[int]:
        return [user.coin for user in self.__users]
    
    @property
    def user_betcoins(self) -> list[int]:
        return [user.betcoin for user in self.__users]
    
    @property
    def user_hands(self) -> list[list[tuple[str, int]]]:
        return [[(card.suit, card.strength) for card in user.hands.hands] for user in self.__users]
    
    @property
    def dealer_hands(self) -> list[tuple[str, int]]:
        return [(card.suit, card.strength) for card in self.__dealer_hands.hands]
    
    @property
    def dealer_strength(self) -> int:
        return self.__dealer_hands.hand_strength
    
    @property
    def user_strengths(self) -> list[int]:
        return [user.hands.hand_strength for user in self.__users]
    
    @property
    def user_names(self) -> list[str]:
        return [user.name for user in self.__users]
    
    @property
    def round(self) -> int:
        return self.__round

