from tkinter import Tk
from PIL import Image, ImageTk

class MainFrame(Tk):
    def __init__(self):
        super().__init__()

        self.title("Twitch Live Downloader")
        self.geometry("700x310")
        self.resizable(False, False)
