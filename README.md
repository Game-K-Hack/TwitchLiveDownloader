<p align="center" >
    <img src="./images/icon.png" width=150 />
</p>

<br>

<div align="center">
  <a href="https://github.com/Game-K-Hack/TwitchLiveDownloader/releases/tag/1.0.2">
    <img src="https://img.shields.io/static/v1?label=release&message=v1.0.2&color=blue" alt="Release - v1.0.2" />
  </a>
  <a href="#">
    <img src="https://img.shields.io/static/v1?label=version&message=stable&color=green" alt="Version - Stable" />
  </a>
  <a href="https://choosealicense.com/licenses/mit">
    <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License" />
  </a>
</div>

<h4 align="center">Download Twitch Lives in live</h4>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#installation">Installation</a> •
  <a href="#setting">Setting</a> •
  <a href="#functioning">Functioning</a>
</p>

<br>
<br>

## Description

This interface allows you to download live streams from the Twitch platform in live. This program therefore allows you to download live broadcasts which are not rebroadcast.

## Installation

For this script to work, you must have Python in version 3.9 *(or a higher version)* and have installed the following libraries:

| Name | Installation command |
| ------ | ------ |
| Fake Useragent | `pip install fake-useragent` |
| OpenCV | `pip install opencv-python` |
| Requests | `pip install requests` |
| PyYAML | `pip install PyYAML` |

## Setting

To change the download folder you must click on the text `Output Directory` and select the destination folder or change the configuration file.

### Add Language

To add a new language in this software, nothing could be simpler, just clone a JSON file from another language and modify the language values. The language files are located in the `lang` folder.

### Configuration

You can change the software defaults to avoid changing the values each time you launch. The configuration file is located in the root of the project, the file is `config.yml`. I advise you to configure your token to avoid having to retrieve it each time you launch.

## Functioning

<img src="./images/screenshot.png" alt="Screenshot" />

<p align="left">
    The download button
    <img src="./images/downloads.png" width="25px" alt="Download" />
    , allows you to start downloading the live. If you want to stop the download, a stop button.
    <img src="./images/stop.png" width="25px" alt="Download" />
    is displayed once the program is started.
</p>

The `Values` tab allows you to view the different values of the live, just as the `Status` allows you to see if the program is downloading a live or not. The `Time` allows you to know the downloaded video time *(this does not indicate the live time)* and `Size` is the size of the downloaded video. `Execution Time` allows you to know the execution time and download time.
`Action` allows you to see the actions performed by the software.
