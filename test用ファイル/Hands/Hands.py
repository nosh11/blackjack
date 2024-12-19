
class Hands:
    def __init__(self):
        self.hands = []
        self.hands_strength = 0
    
    def clear_hands(self):
        self.hands = []

    def add_hands(self, egara:str, suuji:int): #??????????
        self.hands.append((egara, suuji))

    def get_hands_list(self):
        return self.hands

    def cal_hands_strength(self):
        self.hands_strength = 0
        ace_count = 0

        for hand in [hand[1] for hand in self.hands]:
            if hand == 'A':
                ace_count = ace_count + 1
            else:
                if hand in ['J', 'Q', 'K']:
                    self.hands_strength += 10
                else:
                    self.hands_strength += int(hand)

        for _ in range(ace_count):
            if self.hands_strength < 11:
                self.hands_strength += 11
            else:
                self.hands_strength += 1


    def get_hands_strength(self):
        return self.hands_strength

