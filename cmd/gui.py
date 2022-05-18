import sys
import os
from tkinter import *

root = Tk()

root.title("Synthetic Data with ThreeDWorld")

def run():
    os.system('python3 src\scene.py')

btn = Button(root, text="Run", command=run)
btn.pack()

root.mainloop()