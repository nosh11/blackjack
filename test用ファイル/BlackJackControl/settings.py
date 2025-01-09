import os


FONTS = ["Yu Mincho"]
FONT_IDX = 0
PATH = os.path.dirname(__file__).replace("\\", "/")

COLORS = ['#ff0000', '#0000dd', '#cccc00']

STRENGTH = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


MARKS = {
    "spade": ("♠", "black"),
    "heart": ("♥", "red"),
    "diamond": ("♦", "red"),
    "club": ("♣", "black")
}