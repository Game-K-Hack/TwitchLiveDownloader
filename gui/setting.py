from tkinter import LabelFrame, Label, Spinbox, StringVar, Entry, IntVar, Canvas, W, E
from core import Core
import os

class SettingFrame:
    def __init__(self, root):
        self.username = StringVar(value=Core.DEFAULT["username"])
        self.vidname = StringVar(value=Core.DEFAULT["video_name"])
        self.waittime = IntVar(value=int(Core.DEFAULT["wait_time"]))
        self.token = StringVar(value=Core.DEFAULT["access_token"])

        self.labelframe = LabelFrame(
            root, 
            text=Core.LANG["setting"]["label"], 
            padx=10, 
            pady=10)
        self.labelframe.place(x=10, y=10)
        
        label_username = Label(
            self.labelframe, 
            text=Core.LANG["setting"]["username"])
        label_username.grid(row=0, column=0, sticky=E)
        entry_username = Entry(
            self.labelframe, 
            textvariable=self.username, 
            width=25)
        entry_username.grid(row=0, column=1, sticky=W)
        # entry_username.bind("<FocusOut>", self.update_out_path)

        label_vidname = Label(
            self.labelframe, 
            text=Core.LANG["setting"]["videoname"])
        label_vidname.grid(row=1, column=0, sticky=E)
        entry_vidname = Entry(
            self.labelframe, 
            textvariable=self.vidname, 
            width=25)
        entry_vidname.grid(row=1, column=1, sticky=W)
        # entry_vidname.bind("<FocusOut>", self.update_out_path)

        label_waittime = Label(
            self.labelframe, 
            text=Core.LANG["setting"]["waittime"])
        label_waittime.grid(row=2, column=0, sticky=E)
        spinbox_waittime = Spinbox(
            self.labelframe, 
            from_=0, 
            to=30, 
            textvariable=self.waittime, 
            width=23)
        spinbox_waittime.grid(row=2, column=1, sticky=W)
        
        label_token = Label(
            self.labelframe, 
            text=Core.LANG["setting"]["token"])
        label_token.grid(row=3, column=0, sticky=E)
        entry_token = Entry(
            self.labelframe, 
            textvariable=self.token, 
            width=25, 
            show="*")
        entry_token.grid(row=3, column=1, sticky=W)

        Canvas(self.labelframe, width=260, height=0).grid(row=4, column=0, columnspan=2)
