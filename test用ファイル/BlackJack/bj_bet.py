from blackjack import BlackJack
import numpy as np


# (1) bet(0, -10)を実行し、get_user_coinonhand()[0]が "100" であるか
# get_user_betcoin()[0]が10であるか
# (2) bet(1, 10)を10回実行し、get_user_coinonhand()[1]が”0”であるか
# get_user_betcoin()[1]が110であるか
# (3) bet(1, 10)を11回実行し、get_user_coinonhand()[1]が”0”であるか
# get_user_betcoin()[1]が110であるか
# (4) bet(1,10), bet(1,10), bet(1, -10)を実行し、get_user_coinonhand()[1]が”90”であるか
# get_user_betcoin()[1]が20であるか


# (1)
def test_1():
    bj = BlackJack()
    bj.bet(0, -10)
    assert bj.get_user_coinonhand()[0] == 100
    assert bj.get_user_betcoin()[0] == 10
    print("test_1 passed")

# (2)
def test_2():
    bj = BlackJack()
    for _ in range(10):
        bj.bet(1, 10)
    assert bj.get_user_coinonhand()[1] == 0
    assert bj.get_user_betcoin()[1] == 110
    print("test_2 passed")

# (3)
def test_3():
    bj = BlackJack()
    for _ in range(11):
        bj.bet(1, 10)
    assert bj.get_user_coinonhand()[1] == 0
    assert bj.get_user_betcoin()[1] == 110
    print("test_3 passed")

# (4)
def test_4():
    bj = BlackJack()
    bj.bet(1, 10)
    bj.bet(1, 10)
    bj.bet(1, -10)
    assert bj.get_user_coinonhand()[1] == 90
    assert bj.get_user_betcoin()[1] == 20
    print("test_4 passed")

test_1()
test_2()
test_3()
test_4()


