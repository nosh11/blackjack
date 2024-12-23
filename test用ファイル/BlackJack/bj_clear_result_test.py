from blackjack import BlackJack

a = BlackJack()
a.start()
a.clear_result()
print(a.get_user_coinonhand())
print(a.get_user_betcoin())
print(a.get_user_hands())
print(a.get_dealer_hand())