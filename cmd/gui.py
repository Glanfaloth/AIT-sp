import random
import os
from tkinter import *
from tkinter import font as tkfont
class TDWApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageBathroom, PageOffice):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Synthetic Data with ThreeDWorld", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Go to the Bathroom",
                            command=lambda: controller.show_frame("PageBathroom"))
        button2 = Button(self, text="Go to the Office",
                            command=lambda: controller.show_frame("PageOffice"))
        button1.pack()
        button2.pack()

class PageBathroom(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page bathroom", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
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

        sinkLabel = Label(self, text="Select a sink", fg="blue")
        sinkLabel.pack()

        for text, name in SINKS:
            Radiobutton(self, text=text, variable=sink, value=name).pack(anchor=W)

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

        toothbrushLabel = Label(self, text="Select a toothbrush", fg="blue")
        toothbrushLabel.pack()

        for text, name in TOOTHBRUSHS:
            Radiobutton(self, text=text, variable=toothbrush, value=name).pack(anchor=W)

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


        btn = Button(self, text="Run", command=lambda: click(sink.get(), toothbrush.get()))
        btn.pack()

class PageOffice(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page office", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
    app = TDWApp()
    app.mainloop()