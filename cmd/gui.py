import random
import os
from tkinter import *
from tdw.librarian import ModelLibrarian

librarian = ModelLibrarian()
root = Tk()

root.title("Synthetic Data with ThreeDWorld")

# select a cup
cups = librarian.get_all_models_in_wnid("n03147509")  # cup
CUP_NAMES = [record.name for record in cups if not record.do_not_use]
CUP_NAMES.insert(0, "random")

cup = StringVar()
cup.set("random")

cupLabel = Label(root, text="Select a cup", fg="blue")
cupLabel.pack()

for name in CUP_NAMES:
    Radiobutton(root, text=name, variable=cup, value=name).pack(anchor=W)

# select a fruit
FRUIT_NAMES = [
    "apple",
    "b03_banana_01_high",
    "b04_banana",
    "banana_fix2",
    "orange",
    "b04_orange_00",
]

FRUITS = [
    ("random", "random"),
    ("apple", "apple"),
    ("banana1", "b03_banana_01_high"),
    ("banana2", "b04_banana"),
    ("banana3", "banana_fix2"),
    ("orange1", "orange"),
    ("orange2", "b04_orange_00"),
    ("none", "none"),
]

fruit = StringVar()
fruit.set("random")

fruitLabel = Label(root, text="Select a fruit", fg="blue")
fruitLabel.pack()

for text, name in FRUITS:
    Radiobutton(root, text=text, variable=fruit, value=name).pack(anchor=W)

# select a bread
BREAD_NAMES = ["bread", "b03_loafbread", "b03_burger"]
BREADS = [
    ("random", "random"),
    ("bread", "bread"),
    ("loafbread", "b03_loafbread"),
    ("burger", "b03_burger"),
    ("none", "none"),
]
bread = StringVar()
bread.set("random")

breadLabel = Label(root, text="Select a bread", fg="blue")
breadLabel.pack()

for text, name in BREADS:
    Radiobutton(root, text=text, variable=bread, value=name).pack(anchor=W)

PASS_MASKS = [("img", "_img"), ("id", "_id"), ("depth", "_depth")]

# add a button to run the program
def click(cupValue, fruitValue, breadValue):
    cupArg = ""
    if cupValue == "random":
        cupValue = random.choice(CUP_NAMES)
        cupArg = " --cup " + cupValue
    elif cupValue != "":
        cupArg = " --cup " + cupValue
    fruitArg = ""
    if fruitValue == "random":
        fruitValue = random.choice(FRUIT_NAMES)
        fruitArg = " --fruit " + fruitValue
    elif fruitValue != "":
        fruitArg = " --fruit " + fruitValue
    breadArg = ""
    if breadValue == "random":
        breadValue = random.choice(BREAD_NAMES)
        breadArg = " --bread " + breadValue
    elif breadValue != "":
        breadArg = " --bread " + breadValue
    os.system("python3 src\test.py" + cupArg + fruitArg + breadArg)


btn = Button(root, text="Run", command=lambda: click(cup.get(), fruit.get(), bread.get()))
btn.pack()

root.mainloop()
