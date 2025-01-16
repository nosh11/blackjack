import random

class Cards:
    def __init__(self):
        self.__deck = []
        self.reset_card()
    
    def draw_card(self):
        try:
            draw = self.__deck.pop(random.randrange(len(self.__deck)))
        except(ValueError):
            print('カードがありません')
        return draw

    def reset_card(self):
        self.__deck.clear()
        suit = ['spade', 'club', 'heart', 'diamond']
        number = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        for su in suit:
            for num in number:
                self.__deck.append((su, num))

    def get_deck(self):
        return self.__deck
