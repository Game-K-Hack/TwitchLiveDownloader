from tkinter import LabelFrame, Label, Spinbox, StringVar, Entry, IntVar
from core import Core
import os

class SettingFrame:
    def __init__(self, root):
        self.username = StringVar(value=Core.DEFAULT["username"])
        self.vidname = StringVar(value=Core.DEFAULT["video_name"])
        self.waittime = IntVar(value=int(Core.DEFAULT["wait_time"]))
        self.apikey = StringVar(value=Core.DEFAULT["access_token"])

        self.labelframe = LabelFrame(
            root, 
            text=Core.LANG["setting"]["label"], 
            padx=10, 
            pady=10)
        self.labelframe.place(x=10, y=10)
        
        label_username = Label(
            self.labelframe, 
            text=Core.LANG["setting"]["username"])
        label_username.grid(row=0, column=0)
        entry_username = Entry(
            self.labelframe, 
            textvariable=self.username, 
            width=30)
        entry_username.grid(row=0, column=1)
        # entry_username.bind("<FocusOut>", self.update_out_path)

        label_vidname = Label(
            self.labelframe, 
            text=Core.LANG["setting"]["videoname"])
        label_vidname.grid(row=1, column=0)
        entry_vidname = Entry(
            self.labelframe, 
            textvariable=self.vidname, 
            width=30)
        entry_vidname.grid(row=1, column=1)
        # entry_vidname.bind("<FocusOut>", self.update_out_path)

        label_waittime = Label(
            self.labelframe, 
            text=Core.LANG["setting"]["waittime"])
        label_waittime.grid(row=2, column=0)
        spinbox_waittime = Spinbox(
            self.labelframe, 
            from_=0, 
            to=30, 
            textvariable=self.waittime, 
            width=28)
        spinbox_waittime.grid(row=2, column=1)
        
        label_apikey = Label(
            self.labelframe, 
            text=Core.LANG["setting"]["apikey"])
        label_apikey.grid(row=3, column=0)
        entry_apikey = Entry(
            self.labelframe, 
            textvariable=self.apikey, 
            width=30, 
            show="*")
        entry_apikey.grid(row=3, column=1)

    # def update_out_path(self, pos=None):
    #     Core.out_path.set(os.path.join(Core.out_path, self.username.get(), self.vidname.get()).replace("\\", "/"))
