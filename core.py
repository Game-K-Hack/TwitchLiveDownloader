import os
import yaml
from fake_useragent import UserAgent
from tkinter import StringVar

with open("./config.yml", "r") as stream:
    yml = yaml.safe_load(stream)

class Core:
    LANG_PATH = os.path.join(os.path.realpath("./lang"), f"lang-{yml['lang']}.json")
    LANG:dict = eval(open(LANG_PATH, "r", encoding="utf8").read())
    UA = UserAgent().firefox
    DEFAULT:dict = yml["default"]
    CLIENT_ID:str = yml["client_id"]
    ACCESS_KEY:str = DEFAULT["access_token"]
    VERIFY:bool = True
    ACCESS_REQUEST:dict = {
        "operationName":"PlaybackAccessToken_Template", 
        "query":"query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {  streamPlaybackAccessToken(channelName: $login, params: {platform: \"web\", playerBackend: \"mediaplayer\", playerType: $playerType}) @include(if: $isLive) {    value    signature    __typename  }  videoPlaybackAccessToken(id: $vodID, params: {platform: \"web\", playerBackend: \"mediaplayer\", playerType: $playerType}) @include(if: $isVod) {    value    signature    __typename  }}", 
        "variables": {
            "isLive":True, 
            "login":None, 
            "isVod":False, 
            "vodID":"", 
            "playerType":"site"
        }
    }

    out_path:str = ""
    out_filename:str = ""
    out_directory:StringVar
    action:StringVar
