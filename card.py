from settings import STRENGTH
import random

class Card:
    def __init__(self, suit: str, strength: int):
        self.__suit = suit
        self.__strength = strength

    @property
    def suit(self):
        return self.__suit
    
    @property
    def strength(self):
        return self.__strength


class Deck:
    def __init__(self):
        self.__cards: list[Card] = []
        self.reset_card()
    
    def draw_card(self) -> Card:
        draw = self.__cards.pop(0)
        return draw

    def reset_card(self):
        self.__cards.clear()
        for suit in ['spade', 'club', 'heart', 'diamond']:
            for num in range(1, 14):
                self.__cards.append(Card(suit, num))
        random.shuffle(self.__cards)
