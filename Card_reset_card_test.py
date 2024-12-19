import random

class Cards:
    def __init__(self):
        self.__deck = []
        #self.reset_card()
    
    def draw_card(self):
        draw = self.__deck.pop(random.randrange(len(self.__deck)))
        return draw

    def reset_card(self):
        self.__deck.clear()
        suit = ['spade', 'club', 'heart', 'diamond']
        number = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        for su in suit:
            for num in number:
                self.__deck.append((su, num))

    def get_deck(self):#テスト用ゲッター
        return self.__deck
    

A = Cards()
print(A.get_deck())
A.reset_card()
print(len(A.get_deck()))
print(A.get_deck())