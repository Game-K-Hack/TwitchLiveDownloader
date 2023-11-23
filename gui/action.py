from tkinter import LabelFrame, Label, StringVar, Canvas, W, E, filedialog
from tkinter import messagebox
from core import Core

class ActionFrame:
    def __init__(self, root):
        Core.action = StringVar()
        Core.out_directory = StringVar(value=Core.out_path)

        self.labelframe = LabelFrame(
            root, 
            borderwidth=0, 
            padx=10, 
            pady=10)
        self.labelframe.place(x=10, y=245)

        Canvas(self.labelframe, width=500, height=0).grid(row=0, column=2)

        cnv = Canvas(self.labelframe, width=500, height=15, cursor="hand2")
        cnv.grid(row=1, column=1, columnspan=2)
        cnv.bind("<Button-1>", self.browse_file)

        labeloutdir = Label(self.labelframe, text=Core.LANG["outdir"] + " :", cursor="hand2")
        labeloutdir.grid(row=1, column=1, sticky=E)
        labeloutdir.bind("<Button-1>", self.browse_file)

        Core.out_directory.set(Core.out_path)
        labelaction = Label(self.labelframe, textvariable=Core.out_directory, cursor="hand2")
        labelaction.grid(row=1, column=2, sticky=W)
        labelaction.bind("<Button-1>", self.browse_file)

        label_action = Label(
            self.labelframe, 
            text=Core.LANG["action"]["label"] + " :")
        label_action.grid(row=2, column=1, sticky=E)
        label_action_val = Label(
            self.labelframe, 
            textvariable=Core.action)
        label_action_val.grid(row=2, column=2, sticky=W)

        Canvas(self.labelframe, width=400, height=0).grid(row=3, column=1, columnspan=2)

    def browse_file(self, event:any=None):
        path = filedialog.askdirectory()
        if path == "":
            if Core.out_path == "":
                messagebox.showwarning(*Core.LANG["error"]["no_path_set"])
        else:
            Core.out_path = path
            Core.out_directory.set(path)