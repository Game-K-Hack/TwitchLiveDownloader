from tkinter import LabelFrame, Label, StringVar, Canvas, W, E
from core import Core
import os

class ValueFrame:
    def __init__(self, root):
        self.status = StringVar(value=Core.LANG["stop"])
        self.time = StringVar()
        self.size = StringVar()
        self.executiontime = StringVar()

        self.labelframe = LabelFrame(
            root, 
            text=Core.LANG["value"]["label"], 
            width=280, 
            height=113)
        self.labelframe.place(x=10, y=140)

        Canvas(self.labelframe, width=150, height=0).grid(row=0, column=2)

        label_status = Label(self.labelframe, text=Core.LANG["value"]["status"] + " :")
        label_status.grid(row=1, column=1, sticky=E)
        self.label_status_val = Label(self.labelframe, textvariable=self.status, fg="red")
        self.label_status_val.grid(row=1, column=2, sticky=W)

        label_time = Label(self.labelframe, text=Core.LANG["value"]["time"] + " :")
        label_time.grid(row=2, column=1, sticky=E)
        label_time_val = Label(self.labelframe, textvariable=self.time)
        label_time_val.grid(row=2, column=2, sticky=W)

        label_size = Label(self.labelframe, text=Core.LANG["value"]["size"] + " :")
        label_size.grid(row=3, column=1, sticky=E)
        label_size_val = Label(self.labelframe, textvariable=self.size)
        label_size_val.grid(row=3, column=2, sticky=W)

        label_execution = Label(self.labelframe, text=Core.LANG["value"]["executiontime"] + " :")
        label_execution.grid(row=4, column=1, sticky=E)
        label_execution_val = Label(self.labelframe, textvariable=self.executiontime)
        label_execution_val.grid(row=4, column=2, sticky=W)

        Canvas(self.labelframe, width=280, height=2).grid(row=5, column=1, columnspan=2)

    def set_status(self, is_download:bool) -> None:
        if is_download:
            self.status.set(Core.LANG["status"]["download"] + "...")
            self.label_status_val.configure(fg="orange")
        else:
            self.status.set(Core.LANG["status"]["stop"])
            self.label_status_val.configure(fg="red")
