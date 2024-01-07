from gui.main import MainFrame
from gui.setting import SettingFrame
from gui.value import ValueFrame
from gui.video import VideoFrame
from gui.action import ActionFrame
from downloader import Downloader
from tkinter import PhotoImage, Button, messagebox
from threading import Thread
from core import Core
import os

root = MainFrame()
af = ActionFrame(root)
sf = SettingFrame(root)
valf = ValueFrame(root)
vidf = VideoFrame(root)

# load images
default_img = PhotoImage(file=Core.DEFAULT["image"]).subsample(5)
vidf.photo.configure(image=default_img)
vidf.photo.image = default_img
download_img = PhotoImage(file="./images/downloads.png")
download_icon = download_img.subsample(15)
stop_image = PhotoImage(file="./images/stop.png")
stop_icon = stop_image.subsample(15)
root.iconbitmap("./images/icon.ico")

def change_status(is_download:bool) -> None:
    dwld.is_start = is_download
    valf.set_status(is_download)
    action_button.configure(image=stop_icon if is_download else download_icon)

dwld = Downloader(change_status=change_status, 
                  value_frame=valf, 
                  video_frame=vidf)

def action_function():
    if action_button.cget("image") == str(download_icon):
        if Core.out_path == "":
            messagebox.showerror(*Core.LANG["error"]["no_path_set"])
            return None
        change_status(True)
        Core.ACCESS_REQUEST["variables"]["login"] = sf.username.get()
        dwld.username = sf.username.get()
        dwld.video_name = sf.vidname.get()
        dwld.access_token = sf.token.get()
        dwld.wait_time = sf.waittime.get()
        dwld.run()
    else:
        change_status(False)

action_button = Button(root, border=0, command=lambda: Thread(target=action_function).start(), cursor="hand2")
action_button.place(x=645, y=260)

action_function()

def close():
    dwld.is_start = False
    root.destroy()
    os.system(f"taskkill /PID {os.getpid()} /F")
    quit()

root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()