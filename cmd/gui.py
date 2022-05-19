import sys
import os
from tkinter import *

from matplotlib.pyplot import grid
from pyparsing import col
root = Tk()

root.title("Synthetic Data with ThreeDWorld")
FRUITS = [
    ("none", "none"),
    ("apple", "apple"),
    ("banana1", "b03_banana_01_high"),
    ("banana2", "b04_banana"),
    ("banana3", "banana_fix2"),
    ("orange", "b04_orange_00"),
]

fruit = StringVar()
fruit.set("none")

fruitLabel = Label(root, text="Select a fruit", fg="blue")
fruitLabel.pack()

for text, name in FRUITS:
    Radiobutton(root, text=text, variable=fruit, value=name).pack(anchor=W)

def click(fruitValue):
    fruitArg = ""
    if fruitValue != "":
        fruitArg = " --fruit " + fruitValue
    os.system("python3 src\office_desk_scene.py" + fruitArg)


btn = Button(root, text="Run", command=lambda: click(fruit.get()))
btn.pack()

root.mainloop()
