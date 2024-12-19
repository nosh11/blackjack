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
        num1 = 0
        self.hands_strength = 0
        ace_count = 0
        while num1 < len(self.hands) - 1:
            if self.hands[num1][1] == 'A':
                ace_count = ace_count + 1
            
            else:
                if self.hands[num1][1] == 'J' or 'Q' or 'K':
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

a = Hands()
print(a.get_hands_list())
a.add_hands('spade', 'A')
print(a.get_hands_list())