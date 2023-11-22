from tkinter import LabelFrame, Label, StringVar
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

        label_status = Label(self.labelframe, text=Core.LANG["value"]["status"] + " : ")
        label_status.place(x=52, y=5)
        self.label_status_val = Label(self.labelframe, textvariable=self.status, fg="red")
        self.label_status_val.place(x=95, y=5)

        label_time = Label(self.labelframe, text=Core.LANG["value"]["time"] + " :")
        label_time.place(x=58, y=25)
        label_time_val = Label(self.labelframe, textvariable=self.time)
        label_time_val.place(x=95, y=25)

        label_size = Label(self.labelframe, text="Size : ")
        label_size.place(x=64, y=45)
        label_size_val = Label(self.labelframe, textvariable=self.size)
        label_size_val.place(x=95, y=45)

        label_execution = Label(self.labelframe, text="Execution time : ")
        label_execution.place(x=5, y=65)
        label_execution_val = Label(self.labelframe, textvariable=self.executiontime)
        label_execution_val.place(x=95, y=65)

    def set_status(self, is_download:bool) -> None:
        if is_download:
            self.status.set("Download...")
            self.label_status_val.configure(fg="orange")
        else:
            self.status.set("Stop")
            self.label_status_val.configure(fg="red")
