import sys
import os
from tkinter import *

from matplotlib.pyplot import grid
from pyparsing import col

root = Tk()

root.title("Synthetic Data with ThreeDWorld")

# select a fruit
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

# select a bread
BREADS = [
    ("none", "none"),
    ("bread", "bread"),
    ("loafbread", "b03_loafbread"),
    ("burger", "b03_burger"),
]
bread = StringVar()
bread.set("none")

breadLabel = Label(root, text="Select a bread", fg="blue")
breadLabel.pack()

for text, name in BREADS:
    Radiobutton(root, text=text, variable=bread, value=name).pack(anchor=W)

PASS_MASKS = [("img", "_img"), ("id", "_id"), ("depth", "_depth")]

# add a button to run the program
def click(fruitValue, breadValue):
    fruitArg = ""
    breadArg = ""
    if fruitValue != "":
        fruitArg = " --fruit " + fruitValue
    if breadValue != "":
        breadArg = " --bread " + breadValue
    os.system("python3 src\office_scene.py" + fruitArg + breadArg)


btn = Button(root, text="Run", command=lambda: click(fruit.get(), bread.get()))
btn.pack()

root.mainloop()
