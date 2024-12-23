from blackjack import BlackJack
import numpy as np

a = BlackJack()
a.renew_coin(np.array([0,2,1]))
print(a.get_user_coinonhand())
print(a.ranking())
