from Hands import Hands

a = Hands()
a.add_hands('spade', 'A')
a.add_hands('spade', '2')
a.cal_hands_strength()
print(a.get_hands_strength())