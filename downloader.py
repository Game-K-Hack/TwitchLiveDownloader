from core import Core
from gui.value import ValueFrame
from gui.video import VideoFrame
from tkinter import messagebox, PhotoImage
from threading import Thread
import datetime
import requests
import urllib
import utils
import time
import cv2
import re
import os

class Downloader():
    def __init__(self, username:str=None, video_name:str=None, access_token:str=None, wait_time:int=None, change_status:any=None, value_frame:ValueFrame=None, video_frame:VideoFrame=None) -> None:
        self.username:str = username
        self.video_name:str = video_name
        self.access_token:str = access_token
        self.wait_time:int = wait_time
        self.change_status:any = change_status
        self.value_frame:ValueFrame = value_frame
        self.video_frame:VideoFrame = video_frame
        self.is_start = True

    def get_signature(self) -> tuple[str,str]|None:
        Core.action.set(Core.LANG["action"]["get_sig"])
        # get signature of target streamer
        res = requests.post(
            url="https://gql.twitch.tv/gql", 
            headers={
                "Client-ID": Core.CLIENT_ID, 
                "Authorization": f"OAuth {self.access_token}"
            }, 
            json=Core.ACCESS_REQUEST,
            verify=Core.VERIFY
        ).json()
        # keep streamPlaybackAccessToken in data
        res = res["data"]["streamPlaybackAccessToken"]
        # if result is not empty
        if res is not None:
            # get token and signature
            token = res["value"]
            token = urllib.parse.quote(token)
            return token, res["signature"]
        else:
            # if result is empty then stop this loop
            self.change_status(False)
            messagebox.showwarning(*Core.LANG["error"]["streamer_not_found"])
            return None

    def get_all_quality(self, signature:tuple[str,str]) -> str|None:
        Core.action.set(Core.LANG["action"]["get_all_quality"])
        tkn, sig = signature
        # get playlist of stream
        res = requests.get(
            url=f"https://usher.ttvnw.net/api/channel/hls/{Core.ACCESS_REQUEST['variables']['login']}.m3u8?player=twitchweb&token={tkn}&sig={sig}&allow_source=true", 
            verify=Core.VERIFY)
        m3u8 = res.content.decode("utf8")
        # if the error "transcode_does_not_exist" in playlist result
        # and no frame has been retrieved previously
        if "transcode_does_not_exist" in m3u8 and len(self.frames) == 0:
            self.change_status()
            messagebox.showwarning(*Core.LANG["error"]["live_not_found"])
            return None
        else:
            return m3u8

    def get_url_of_best_quality(self, m3u8:str) -> str:
        Core.action.set(Core.LANG["action"]["keep_best_quality"])
        # search best quality
        quality_index, quality_value = None, 0
        # for all lines in playlist to search the best quality
        for index, line in enumerate(m3u8.split("\n")):
            if line.startswith("#EXT-X-STREAM-INF"):
                quality = re.search('RESOLUTION=(.*),CODECS', line, re.IGNORECASE).group(1)
                quality = quality.split("x")
                quality = int(quality[0])*int(quality[1])
                if quality > quality_value:
                    quality_value = quality
                    quality_index = index
        # return best quality and +1 to find stream url
        return m3u8.split("\n")[quality_index+1]
    
    def download(self) -> None:
        # start chronometer
        startime = time.time()
        # get signature of account
        signature = self.get_signature()
        if signature is None or not self.is_start: return None
        # get list all quality of stream
        m3u8 = self.get_all_quality(signature)
        if m3u8 is None or not self.is_start: return None
        # get url of best quality of stream
        url = self.get_url_of_best_quality(m3u8)
        # get playlist of all files type TS
        res = requests.get(url, verify=Core.VERIFY)
        res = res.content.decode("utf8").split("\n")
        # sort result to keep all url of files type TS
        url_list = [res[index+1] for index, line in enumerate(res) if line.startswith("#EXTINF:")]
        self.out_path = f"{Core.out_directory.get()}/{self.username}/{self.video_name}"
        # for all urls, download TS file
        for i in url_list:
            if not self.is_start: return None
            # get content of TS file
            res = requests.get(i, verify=Core.VERIFY).content
            # if the video frame was not downloaded then download
            if res not in self.frames[-15:]:
                self.frames.append(res)
                if not os.path.exists(self.out_path):
                    os.makedirs(self.out_path)
                Core.out_filename = f"{Core.ACCESS_REQUEST['variables']['login']}_{self.index_video}.ts"
                Core.action.set(Core.LANG["action"]["write_to"] + " " + Core.out_filename)
                open(f"{self.out_path}/{Core.out_filename}", "wb").write(res)
                self.index_video += 1
                # calculate difference between end and start time to get time of execution
                self.exectime = time.time() - startime
                # upadte value on interface
                Thread(target=self.update_value).start()

    def run(self) -> None:
        self.frames = []
        self.index_video = 0
        Core.action.set(Core.LANG["action"]["start"])
        while self.is_start:
            # change status to download
            self.change_status(True)
            # download stream
            self.download()
            # 
            self.frames = self.frames[-150:]
            # wait time before
            for i in range(self.wait_time*2):
                # display wait time on interface
                Core.action.set(Core.LANG["action"]["wait"] + " " + str(int(self.wait_time-(i/2))) + " s")
                # wait 0.5 second
                time.sleep(0.5)
                # check if download is cancel
                if not self.is_start:
                    break
        # clear action on interface
        Core.action.set("")
        # change status to stop
        self.change_status(False)

    def update_image(self, video_path) -> None:
        cap = cv2.VideoCapture(video_path)
        images = []
        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break
            else:
                images.append(frame)
        path = os.path.join(os.environ["TEMP"], "TwitchLiveDownloader.tmp.png")
        img = cv2.resize(images[-1], (355, 200))
        cv2.imwrite(path, img)
        img2 = PhotoImage(file=path)
        self.video_frame.photo.configure(image=img2)
        self.video_frame.photo.image = img2

    def update_value(self) -> None:
        # update execution time value
        self.value_frame.executiontime.set(str(round(self.exectime, 5)) + " s")
        # update time value
        t = len([i for i in os.listdir(self.out_path) if i.endswith(".ts")]) * 2
        t = str(datetime.timedelta(seconds=t))
        self.value_frame.time.set(t)
        # update size value
        s = sum([os.path.getsize(os.path.join(self.out_path, i)) for i in os.listdir(self.out_path) if i.endswith(".ts")])
        self.value_frame.size.set(utils.humanbytes(s))
        # update image
        self.update_image(f"{self.out_path}/{Core.out_filename}")
