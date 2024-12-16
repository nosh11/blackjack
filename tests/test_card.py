from src.card import Card, Deck


def test_card_initialization():
    card = Card("Hearts", 5)
    assert card.suit == "Hearts"
    assert card.strength == 5

def test_card_suit():
    card = Card("Spades", 10)
    assert card.suit == "Spades"

def test_card_strength():
    card = Card("Diamonds", 12)
    assert card.strength == 12

def test_deck_initialization():
    deck = Deck()
    assert len(deck._Deck__cards) == 52

def test_deck_draw_card():
    deck = Deck()
    card = deck.draw_card()
    assert isinstance(card, Card)
    assert len(deck._Deck__cards) == 51

def test_deck_reset_card():
    deck = Deck()
    deck.draw_card()
    deck.reset_card()
    assert len(deck._Deck__cards) == 52

def test_deck_shuffle():
    deck = Deck()
    first_card = deck._Deck__cards[0]
    deck.reset_card()
    assert deck._Deck__cards[0] != first_card

if __name__ == "__main__":
    test_card_initialization()
    test_card_suit()
    test_card_strength()
    test_deck_initialization()
    test_deck_draw_card()
    test_deck_reset_card()
    test_deck_shuffle()
    print("All tests passed!")
