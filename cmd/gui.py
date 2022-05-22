import random
import os
from tkinter import *
from tkinter import font as tkfont
from tdw.librarian import ModelLibrarian
librarian = ModelLibrarian()

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
        button3 = Button(self, text="Go to the Kitchen",
                            command=lambda: controller.show_frame("PageKitchen"))
        button1.pack()
        button2.pack()
        button3.pack()

class PageBathroom(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is a bathroom", font=controller.title_font)
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
        label = Label(self, text="This is an office", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        # select a cup
        cups = librarian.get_all_models_in_wnid("n03147509")  # cup
        CUP_NAMES = [record.name for record in cups if not record.do_not_use]
        CUP_NAMES.insert(0, "random")

        cup = StringVar()
        cup.set("random")

        cupLabel = Label(self, text="Select a cup", fg="blue")
        cupLabel.pack()

        for name in CUP_NAMES:
            Radiobutton(self, text=name, variable=cup, value=name).pack(anchor=W)

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

        fruitLabel = Label(self, text="Select a fruit", fg="blue")
        fruitLabel.pack()

        for text, name in FRUITS:
            Radiobutton(self, text=text, variable=fruit, value=name).pack(anchor=W)

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

        breadLabel = Label(self, text="Select a bread", fg="blue")
        breadLabel.pack()

        for text, name in BREADS:
            Radiobutton(self, text=text, variable=bread, value=name).pack(anchor=W)

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
            os.system("python3 src\scene_office.py" + cupArg + fruitArg + breadArg)


        btn = Button(self, text="Run", command=lambda: click(cup.get(), fruit.get(), bread.get()))
        btn.pack()

class PageKitchen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is a kitchen", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        # select a kitchen sink
        SINK_NAMES = [
            "sink_cabinet_unit_wood_beech_honey_chrome_composite",
            "sink_cabinet_unit_wood_oak_white_chrome_composite",
        ]

        SINKS = [
            ("random", "random"),
            ("beech", "sink_cabinet_unit_wood_beech_honey_chrome_composite"),
            ("oak", "sink_cabinet_unit_wood_oak_white_chrome_composite"),
        ]

        sink = StringVar()
        sink.set("random")

        sinkLabel = Label(self, text="Select a sink", fg="blue")
        sinkLabel.pack()

        for text, name in SINKS:
            Radiobutton(self, text=text, variable=sink, value=name).pack(anchor=W)

        # select a microwave
        MICROWAVE_NAMES = ["appliance-ge-profile-microwave_composite", "appliance-ge-profile-microwave3_composite", "b05_whirlpool_microwave_wmc30516as_v-ray", "cgaxis_models_10_11_vray", "microwave_composite", "vm_v5_070_composite", "vray_062_composite"]
        MICROWAVES = [
            ("random", "random"),
            ("microwave1", "appliance-ge-profile-microwave_composite"),
            ("microwave2", "appliance-ge-profile-microwave3_composite"),
            ("microwave3", "b05_whirlpool_microwave_wmc30516as_v-ray"),
            ("microwave3", "cgaxis_models_10_11_vray"),
            ("microwave3", "microwave_composite"),
            ("microwave3", "vm_v5_070_composite"),
            ("microwave3", "vray_062_composite"),
        ]
        toothbrush = StringVar()
        toothbrush.set("random")

        toothbrushLabel = Label(self, text="Select a toothbrush", fg="blue")
        toothbrushLabel.pack()

        for text, name in MICROWAVES:
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
                toothbrushValue = random.choice(MICROWAVE_NAMES)
                toothbrushArg = " --toothbrush " + toothbrushValue
            elif toothbrushValue != "":
                toothbrushArg = " --toothbrush " + toothbrushValue
            os.system("python3 src\scene_bathroom.py"  + sinkArg + toothbrushArg)


        btn = Button(self, text="Run", command=lambda: click(sink.get(), toothbrush.get()))
        btn.pack()

if __name__ == "__main__":
    app = TDWApp()
    app.mainloop()