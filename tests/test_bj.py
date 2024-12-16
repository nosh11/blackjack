from src.bj import BlackJack

def test_initialization():
    bj = BlackJack()
    assert bj.round == 1
    assert len(bj.user_coins) == 3
    assert all(coin == 100 for coin in bj.user_coins)
    assert all(betcoin == 10 for betcoin in bj.user_betcoins)

def test_add_round():
    bj = BlackJack()
    bj.add_round()
    assert bj.round == 2

def test_bet():
    bj = BlackJack()
    bj.bet(0, 5)
    assert bj.user_betcoins[0] == 15
    assert bj.user_coins[0] == 95

def test_start():
    bj = BlackJack()
    bj.start()
    assert len(bj.dealer_hands) == 1
    assert all(len(hands) == 1 for hands in bj.user_hands)

def test_hit():
    bj = BlackJack()
    bj.start()
    result = bj.hit(0)
    assert len(bj.user_hands[0]) == 2
    assert result in [True, False]

def test_dealer():
    bj = BlackJack()
    bj.start()
    bj.dealer()
    assert bj.dealer_strength >= 17

def test_renew_coin():
    bj = BlackJack()
    bj.renew_coin([2, 0, 2])
    assert bj.user_coins[0] == 120
    assert bj.user_coins[1] == 100
    assert bj.user_coins[2] == 120

def test_ranking():
    bj = BlackJack()
    ranking = bj.ranking()
    assert len(ranking) == 3
    assert ranking[0][1] >= ranking[1][1] >= ranking[2][1]

def test_judge():
    bj = BlackJack()
    bj.start()
    bj.judge()
    assert all(coin >= 0 for coin in bj.user_coins)

def test_clear_result():
    bj = BlackJack()
    bj.clear_result()
    assert bj.round == 1
    assert all(coin == 100 for coin in bj.user_coins)
    assert all(betcoin == 10 for betcoin in bj.user_betcoins)
    assert len(bj.dealer_hands) == 0
    assert all(len(hands) == 0 for hands in bj.user_hands)


if __name__ == "__main__":
    test_initialization()
    test_add_round()
    test_bet()
    test_start()
    test_hit()
    test_dealer()
    test_renew_coin()
    test_ranking()
    test_judge()
    test_clear_result()
    print("All tests passed!")