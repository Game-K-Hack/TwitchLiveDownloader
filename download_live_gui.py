from threading import Thread
from tkinter import * 
from tkinter import filedialog
import requests
import datetime
import time
import cv2
import re
import os

is_start = False
out_dir_path = ""

def __close__():
    global is_start
    is_start = False
    root.destroy()
    os.system(f"taskkill /PID {os.getpid()} /F")

def update_image(file):
    cap = cv2.VideoCapture(file)
    images = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        else:
            images.append(frame)
    path = os.path.join(os.environ["TEMP"], "tempImage.png")
    img = cv2.resize(images[-1], (355, 200))
    cv2.imwrite(path, img)
    img2 = PhotoImage(file=path)
    video.configure(image=img2)
    video.image = img2

def humanbytes(B):
    """
    https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb#answer-31631711

    Return the given bytes as a human friendly KB, MB, GB, or TB string.
    """
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)

# def _start_pub_remover():
#     os.system(f"cd {os.path.dirname(__file__)} && start /b python farmer.py")

# def _stop_pub_remover():
#     pid = open('./pid', 'r', encoding='utf8').read()
#     os.system(f"taskkill /PID {pid} /F")

def _check_var():
    ok = True
    if username_value.get() == "":
        l_username.configure(fg="red")
        ok = False
    else:
        l_username.configure(fg="black")
    l_username.update()
    if vidname_value.get() == "":
        l_vidname.configure(fg="red")
        ok = False
    else:
        l_vidname.configure(fg="black")
    l_vidname.update()
    return ok

def _status(is_download):
    if is_download:
        status_value.set("Download...")
        l_status.configure(fg="orange")
    else:
        status_value.set("Stop")
        l_status.configure(fg="red")

def _time(path):
    t = len([i for i in os.listdir(path) if i.endswith(".ts")]) * 2
    t = str(datetime.timedelta(seconds=t))
    time_value.set(t)
    l_time.update()

def _size(path):
    s = sum([os.path.getsize(os.path.join(path, i)) for i in os.listdir(path) if i.endswith(".ts")])
    size_value.set(humanbytes(s))
    l_size.update()

def _exet(val):
    exet_value.set(str(round(val, 5)) + " s")
    l_exet.update()

def download(channel_name, id_vid):
    global is_start, out_dir_path
    nami = 0
    # Renseignez votre client ID Twitch, votre secret client Twitch et le nom de la chaîne Twitch que vous souhaitez regarder
    client_id = "kimne78kx3ncx6brgo4mv6wki5h1ko"
    access_token = apikey_value.get()
    out_dir_path = os.path.join(out_dir_path, e_username.get(), i_vidname.get())

    _status(True)
    nberr = 0
    ultim = []

    while is_start:
        try:
            st = time.time()

            res = requests.post(
                "https://gql.twitch.tv/gql", 
                headers={
                    "Client-ID": client_id, 
                    "Authorization": "OAuth " + access_token
                }, 
                json={
                    "operationName":"PlaybackAccessToken_Template", 
                    "query":"query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {  streamPlaybackAccessToken(channelName: $login, params: {platform: \"web\", playerBackend: \"mediaplayer\", playerType: $playerType}) @include(if: $isLive) {    value    signature    __typename  }  videoPlaybackAccessToken(id: $vodID, params: {platform: \"web\", playerBackend: \"mediaplayer\", playerType: $playerType}) @include(if: $isVod) {    value    signature    __typename  }}", 
                    "variables": {
                        "isLive":True, 
                        "login":channel_name, 
                        "isVod":False, 
                        "vodID":"", 
                        "playerType":"site"
                    }
                },
                verify=False).json()

            token = res["data"]["streamPlaybackAccessToken"]["value"]
            sig = res["data"]["streamPlaybackAccessToken"]["signature"]

            # Obtenez l'URL de lecture en direct
            url = f"https://usher.ttvnw.net/api/channel/hls/{channel_name}.m3u8?player=twitchweb&token={token}&sig={sig}&allow_source=true"
            res = requests.get(url, verify=False)
            m3u8 = res.content.decode("utf8")

            # search best quality
            quality_index = None
            quality_value = 0
            for index, line in enumerate(m3u8.split("\n")):
                if line.startswith("#EXT-X-STREAM-INF"):
                    quality = re.search('RESOLUTION=(.*),CODECS', line, re.IGNORECASE).group(1)
                    quality = quality.split("x")
                    quality = int(quality[0])*int(quality[1])
                    if quality > quality_value:
                        quality_value = quality
                        quality_index = index
            # best quality and +1 to find stream url
            url = m3u8.split("\n")[quality_index+1]

            res = requests.get(url, verify=False)
            res = res.content.decode("utf8").split("\n")

            url_list = [res[index+1] for index, line in enumerate(res) if line.startswith("#EXTINF:")]

            for i in url_list:
                res = requests.get(i, verify=False).content
                if res not in ultim[-15:]:
                    nami += 1
                    ultim.append(res)
                    # path = f"E:/Twitch/{channel_name}/{id_vid}"
                    if not os.path.exists(out_dir_path):
                        os.makedirs(out_dir_path)
                    open(f"{out_dir_path}/{channel_name}_{nami}.ts", "wb").write(res)

            ultim = ultim[-150:]
            # print("[INFO] Time:", time.time()-st)
            _exet(time.time()-st)
            Thread(target=lambda:update_image(f"{out_dir_path}/{channel_name}_{nami}.ts")).start()
            nberr = 0
            _time(out_dir_path)
            _size(out_dir_path)

            for _ in range(int(waittime_value.get())):
                time.sleep(1)
                if not is_start:
                    break

        except Exception as e:
            err = "unsupported operand type(s) for +: 'NoneType' and 'int'"
            if str(e) == err:
                nberr += 1
                time.sleep(1)
            if nberr >= 10:
                _status(False)
                is_start = False
        
    _status(False)

root = Tk()
root.geometry("700x300")
root.resizable(False, False)

def _update_out(pos=None):
    out_value.set(os.path.join(out_dir_path, e_username.get(), i_vidname.get()).replace("\\", "/"))
    l_out.update()

l = LabelFrame(root, text="Setting", padx=10, pady=10)
l.place(x=10, y=10)
username_value = StringVar()
l_username = Label(l, text="Username")
l_username.grid(row=0, column=0)
e_username = Entry(l, textvariable=username_value, width=30)
e_username.grid(row=0, column=1)
e_username.bind("<FocusOut>", _update_out)
vidname_value = StringVar()
l_vidname = Label(l, text="Video name ")
l_vidname.grid(row=1, column=0)
i_vidname = Entry(l, textvariable=vidname_value, width=30)
i_vidname.grid(row=1, column=1)
i_vidname.bind("<FocusOut>", _update_out)
l_waittime = Label(l, text="Wait time")
l_waittime.grid(row=2, column=0)
waittime_value = StringVar(value=3)
s_waittime = Spinbox(l, from_=0, to=30, textvariable=waittime_value, width=28)
s_waittime.grid(row=2, column=1)
apikey_value = StringVar()
l_apikey = Label(l, text="API key")
l_apikey.grid(row=3, column=0)
i_apikey = Entry(l, textvariable=apikey_value, width=30, show="*")
i_apikey.grid(row=3, column=1)
# pubremover_value = IntVar(value=0)
# def _checkbox():
#     if pubremover_value.get():
#         _start_pub_remover()
#     else:
#         _stop_pub_remover()
# cb_pubremover = Checkbutton(l, text="Pub remover", variable=pubremover_value, command=_checkbox)
# cb_pubremover.grid(row=3, column=1)

l = LabelFrame(root, text="Video", padx=10, pady=10)
l.place(x=305, y=10)
photo = PhotoImage(file=os.path.join(os.path.dirname(__file__), "assets", "wallpaper-resized.png"))
video = Label(l, width=355, height=200, image=photo)
video.pack()

l = LabelFrame(root, text="Value", width=280, height=113)
l.place(x=10, y=140)
Label(l, text="Status : ").place(x=52, y=5)
status_value = StringVar()
status_value.set("Stop")
l_status = Label(l, textvariable=status_value, fg="red")
l_status.place(x=95, y=5)
Label(l, text="Time : ").place(x=58, y=25)
time_value = StringVar()
time_value.set("empty")
l_time = Label(l, textvariable=time_value)
l_time.place(x=95, y=25)
Label(l, text="Size : ").place(x=64, y=45)
size_value = StringVar()
size_value.set("empty")
l_size = Label(l, textvariable=size_value)
l_size.place(x=95, y=45)
Label(l, text="Execution time : ").place(x=5, y=65)
exet_value = StringVar()
exet_value.set("empty")
l_exet = Label(l, textvariable=exet_value)
l_exet.place(x=95, y=65)

b_exit = Button(root, text="Exit", command=__close__, width=10)
b_exit.place(x=10, y=265)

Label(root, text="Out : ").place(x=100, y=268)
out_value = StringVar()
out_value.set("empty")
l_out = Label(root, textvariable=out_value)
l_out.place(x=130, y=268)
def _browse_file(search=False):
    global out_dir_path
    if search == True:
        out_dir_path = filedialog.askdirectory()
    _update_out()
b_browse = Button(root, text="Browse", command=lambda: _browse_file(True), width=10)
b_browse.place(x=340, y=265)
e_username.bind("<FocusOut>", _browse_file)

def _stop():
    global is_start
    is_start = False
b_exit = Button(root, text="Stop", command=_stop, width=15)
b_exit.place(x=440, y=265)
def _start():
    global is_start
    if not is_start and _check_var():
        is_start = True
        Thread(target=lambda:download(username_value.get(), vidname_value.get())).start()
b_exit = Button(root, text="Download", command=_start, width=15)
b_exit.place(x=570, y=265)

root.protocol("WM_DELETE_WINDOW", __close__)
root.mainloop()
