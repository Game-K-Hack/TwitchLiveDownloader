from tkinter import Tk

class MainFrame(Tk):
    def __init__(self):
        super().__init__()

        self.title("Title")
        self.geometry("700x310")
        self.resizable(False, False)

        # ico = Image.open("./icon.png")
        # photo = ImageTk.PhotoImage(ico)
        # root.wm_iconphoto(False, photo)

        # root.iconbitmap("./icon.ico")