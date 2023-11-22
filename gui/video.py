from tkinter import LabelFrame, Label, PhotoImage
from core import Core
import os

class VideoFrame:
    def __init__(self, root):
        self.labelframe = LabelFrame(
            root, 
            text=Core.LANG["video"], 
            padx=10, 
            pady=10)
        self.labelframe.place(x=305, y=10)
        self.photo = Label(
            self.labelframe, 
            width=355, 
            height=200)
        self.photo.pack()
