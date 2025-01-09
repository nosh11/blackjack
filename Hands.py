
class Hands:
    def __init__(self):
        self.hands = []
        self.hands_strength = 0
    
    def clear_hands(self):
        self.hands = []

    def add_hands(self, card: tuple[str, str]): #??????????
        self.hands.append(card)

    def get_hands_list(self):
        return self.hands

    def cal_hands_strength(self):
        num1 = 0
        self.hands_strength = 0
        ace_count = 0
        while num1 < len(self.hands):
            if self.hands[num1][1] == 'A':
                ace_count = ace_count + 1
            
            else:
                if self.hands[num1][1] == 'J' or self.hands[num1][1] =='Q' or self.hands[num1][1] == 'K':
                    self.hands_strength = self.hands_strength + 10
                
                else:
                    self.hands_strength = self.hands_strength + int(self.hands[num1][1])
            
            num1 = num1 + 1
        
        num2 = 0
        while num2 < ace_count:
            if self.hands_strength < 11:
                self.hands_strength = self.hands_strength + 11

            else:
                self.hands_strength = self.hands_strength + 1
        
            num2 = num2 + 1


    def get_hands_strength(self):
        return self.hands_strength
