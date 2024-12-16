import unittest
from src.hand import Hands
from src.card import Card

class TestHands(unittest.TestCase):

    def setUp(self):
        self.hands = Hands()

    def test_initial_hands_empty(self):
        self.assertEqual(len(self.hands.hands), 0)

    def test_add_hands(self):
        card = Card('Hearts', 2)
        self.hands.add_hands(card)
        self.assertEqual(len(self.hands.hands), 1)
        self.assertEqual(self.hands.hands[0], card)

    def test_clear_hands(self):
        card = Card('Hearts', 2)
        self.hands.add_hands(card)
        self.hands.clear_hands()
        self.assertEqual(len(self.hands.hands), 0)

    def test_hand_strength(self):
        card1 = Card('Hearts', 2)
        card2 = Card('Spades', 3)
        self.hands.add_hands(card1)
        self.hands.add_hands(card2)
        self.assertEqual(self.hands.hand_strength, 5)

if __name__ == '__main__':
    unittest.main()