import yaml
from fake_useragent import UserAgent

with open("./config.yml", "r") as stream:
    yml = yaml.safe_load(stream)

class Core:
    UA = UserAgent().firefox
    CLIENT_ID = yml["client_id"]
    ACCESS_KEY = yml["access_token"]
    VERIFY = False

    ACCESS_REQUEST = {
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
