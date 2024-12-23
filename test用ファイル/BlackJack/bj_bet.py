from blackjack import BlackJack
import numpy as np

bj = BlackJack()


bj.bet(0, 10)
bj.bet(1, 20)
bj.bet(2, 30)


print(bj.get_user_betcoin())
print(bj.get_user_coinonhand())

assert bj.get_user_betcoin() == np.array([10, 20, 30])
assert bj.get_user_coinonhand() == [100, 90, 80]
bj.get_user_betcoin()



