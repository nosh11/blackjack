import os


FONTS = ["Yu Mincho"]
FONT_IDX = 0
PATH = os.path.dirname(__file__).replace("\\", "/")

COLORS = ['#ff0000', '#0000dd', '#cccc00']

STRENGTH = {
    'A': 1,
    **{str(x): x for x in range(2, 11)},
    'J': 11,
    'Q': 12,
    'K': 13
}
