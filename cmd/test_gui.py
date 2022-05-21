import random
import os
from tkinter import *
from tdw.librarian import ModelLibrarian

librarian = ModelLibrarian()
root = Tk()

root.title("Synthetic Data with ThreeDWorld")

# select a bathroom sink
SINK_NAMES = [
    "sink_cabinet_unit_wood_beech_honey_porcelain_composite",
    "sink_cabinet_unit_wood_oak_white_porcelain_composite",
]

SINKS = [
    ("random", "random"),
    ("beech", "sink_cabinet_unit_wood_beech_honey_porcelain_composite"),
    ("oak", "sink_cabinet_unit_wood_oak_white_porcelain_composite"),
]

sink = StringVar()
sink.set("random")

sinkLabel = Label(root, text="Select a sink", fg="blue")
sinkLabel.pack()

for text, name in SINKS:
    Radiobutton(root, text=text, variable=sink, value=name).pack(anchor=W)

# select a toothbrush
TOOTHBRUSH_NAMES = ["toothbrush", "b03_toothbrush", "generic_toothbrush_001"]
TOOTHBRUSHS = [
    ("random", "random"),
    ("toothbrush1", "toothbrush"),
    ("toothbrush2", "b03_toothbrush"),
    ("toothbrush3", "generic_toothbrush_001"),
]
toothbrush = StringVar()
toothbrush.set("random")

toothbrushLabel = Label(root, text="Select a toothbrush", fg="blue")
toothbrushLabel.pack()

for text, name in TOOTHBRUSHS:
    Radiobutton(root, text=text, variable=toothbrush, value=name).pack(anchor=W)

PASS_MASKS = [("img", "_img"), ("id", "_id"), ("depth", "_depth")]

# add a button to run the program
def click(sinkValue, toothbrushValue):
    sinkArg = ""
    if sinkValue == "random":
        sinkValue = random.choice(SINK_NAMES)
        sinkArg = " --sink " + sinkValue
    elif sinkValue != "":
        sinkArg = " --sink " + sinkValue
    toothbrushArg = ""
    if toothbrushValue == "random":
        toothbrushValue = random.choice(TOOTHBRUSH_NAMES)
        toothbrushArg = " --toothbrush " + toothbrushValue
    elif toothbrushValue != "":
        toothbrushArg = " --toothbrush " + toothbrushValue
    os.system("python3 src\scene_bathroom.py"  + sinkArg + toothbrushArg)


btn = Button(root, text="Run", command=lambda: click(sink.get(), toothbrush.get()))
btn.pack()

root.mainloop()
