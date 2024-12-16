import unittest
import os
from src import settings

class TestSettings(unittest.TestCase):

    def test_fonts(self):
        self.assertIn("Yu Mincho", settings.FONTS)
        self.assertEqual(settings.FONT_IDX, 0)

    def test_path(self):
        expected_path = os.path.dirname(settings.__file__).replace("\\", "/")
        self.assertEqual(settings.PATH, expected_path)

    def test_colors(self):
        self.assertEqual(settings.COLORS, ['#ff0000', '#0000dd', '#cccc00'])

    def test_strength(self):
        expected_strength = {
            'A': 1,
            **{str(x): x for x in range(2, 11)},
            'J': 11,
            'Q': 12,
            'K': 13
        }
        self.assertEqual(settings.STRENGTH, expected_strength)

if __name__ == '__main__':
    unittest.main()