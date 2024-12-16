from src.user import User
import unittest
from src.hand import Hands
class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(name="Alice", coin=100, betcoin=10)

    def test_initialization(self):
        self.assertEqual(self.user.name, "Alice")
        self.assertEqual(self.user.coin, 100)
        self.assertEqual(self.user.betcoin, 10)
        self.assertIsInstance(self.user.hands, Hands)

    def test_set_coin(self):
        self.user.coin = 150
        self.assertEqual(self.user.coin, 150)

    def test_set_betcoin(self):
        self.user.betcoin = 20
        self.assertEqual(self.user.betcoin, 20)

if __name__ == '__main__':
    unittest.main()
