from card import Card

class Hands:
    def __init__(self):
        self.__hands: list[Card] = []

    def clear_hands(self):
        self.__hands = []

    def add_hands(self, card):
        self.__hands.append(card)


    @property
    def hands(self):
        return self.__hands

    @property
    def hand_strength(self):
        return sum([card.strength for card in self.hands])