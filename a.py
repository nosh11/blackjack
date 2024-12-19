

import tkinter as tk


root = tk.Tk()
root.title("Hello, World!")
root.geometry("800x600")

canvas = tk.Canvas(root, width=800, height=200)

font = ("游明朝", 50)

images = []

for i in range(10):
    canvas.create_text(400 + i * 10, 10 + i * 50, font=font, text=f"♥ ♦ ♣ ♠")

canvas.place(x=0, y=0)

frame = tk.Frame(root)
frame.place(x=0, y=200)

for i in range(10):
    tk.Button(frame, text=f"Button {i}", command=lambda i=i: print(f"Button {i} clicked")).grid(row=0, column=i)

root.mainloop()