import tkinter as tk
from PIL import Image, ImageTk
import random
import os

MARKS = ["club", "diamond", "heart", "spade"]
PATH = os.path.dirname(__file__).replace("\\", "/")

root = tk.Tk()

class CardViewer(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=224, height=320)
        self.index = 0
        self.photos = [None, None]
        self.toggle()

    def draw(self):
        self.delete("all")
        if self.photos[1]:
            self.create_image(122, 170, image=self.photos[1])
        if self.photos[0]:
            self.create_image(102, 150, image=self.photos[0])

    def toggle(self):
        mark = MARKS[random.randint(0, 3)]
        strength = str(random.randint(1, 13)).zfill(2)
        photo = tk.PhotoImage(file=f"{PATH}/cards/card_{mark}_{strength}.png")
        if photo.width() == 136:
            photo = photo.zoom(3).subsample(2)
        self.photos = [photo, self.photos[0]]
        self.draw()

card = CardViewer(root)
card.grid(row=0, column=0, padx=10, pady=10)
tk.Button(root, text="Update", command=card.toggle).grid(row=1, column=0)
root.mainloop()