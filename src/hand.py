from src.card import Card

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
        strength = 0
        ace_count = 0
        for card in self.__hands:
            if card.strength == 1:
                ace_count += 1
            elif card.strength >= 10:
                strength += 10
            else:
                strength += card.strength
        for _ in range(ace_count):
            if strength + 11 <= 21:
                strength += 11
            else:
                strength += 1
        return strength