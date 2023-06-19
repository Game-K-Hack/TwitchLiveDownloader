# -*- coding: utf-8 -*-

import os
open("./pid", "w", encoding="utf8").write(str(os.getpid()))

import logging
from colorama import Fore
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Chat import ChatPresence
from TwitchChannelPointsMiner.classes.Discord import Discord
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings

twitch_miner = TwitchChannelPointsMiner(
    username="verbeo",           # If no password will be provided, the script will ask interactively
    claim_drops_startup=False,                  # If you want to auto claim all drops from Twitch inventory on the startup
    priority=[                                  # Custom priority in this case for example:
        Priority.STREAK,                        # - We want first of all to catch all watch streak from all streamers
        Priority.DROPS,                         # - When we don't have anymore watch streak to catch, wait until all drops are collected over the streamers
        Priority.ORDER                          # - When we have all of the drops claimed and no watch-streak available, use the order priority (POINTS_ASCENDING, POINTS_DESCEDING)
    ],
    enable_analytics=False,                     # Disables Analytics if False. Disabling it significantly reduces memory consumption
    disable_ssl_cert_verification=False,        # Set to True at your own risk and only to fix SSL: CERTIFICATE_VERIFY_FAILED error
    logger_settings=LoggerSettings(
        save=True,                              # If you want to save logs in a file (suggested)
        console_level=logging.INFO,             # Level of logs - use logging.DEBUG for more info
        console_username=False,                 # Adds a username to every console log line if True. Useful when you have many open consoles with different accounts
        auto_clear=True,                        # Create a file rotation handler with interval = 1D and backupCount = 7 if True (default)
        time_zone="",                           # Set a specific time zone for console and file loggers. Use tz database names. Example: "America/Denver"
        file_level=logging.DEBUG,               # Level of logs - If you think the log file it's too big, use logging.INFO
        emoji=True,                             # On Windows, we have a problem printing emoji. Set to false if you have a problem
        less=False,                             # If you think that the logs are too verbose, set this to True
        colored=True,                           # If you want to print colored text
        color_palette=ColorPalette(             # You can also create a custom palette color (for the common message).
            STREAMER_online="GREEN",            # Don't worry about lower/upper case. The script will parse all the values.
            streamer_offline="red",             # Read more in README.md
            BET_wiN=Fore.MAGENTA                # Color allowed are: [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET].
        )
    ),
    streamer_settings=StreamerSettings(
        make_predictions=False,                 # If you want to Bet / Make prediction
        follow_raid=True,                       # Follow raid to obtain more points
        claim_drops=True,                       # We can't filter rewards base on stream. Set to False for skip viewing counter increase and you will never obtain a drop reward from this script. Issue #21
        claim_moments=True,                     # If set to True, https://help.twitch.tv/s/article/moments will be claimed when available
        watch_streak=True,                      # If a streamer go online change the priority of streamers array and catch the watch screak. Issue #11
        chat=ChatPresence.ONLINE                # Join irc chat to increase watch-time [ALWAYS, NEVER, ONLINE, OFFLINE]
    )
)

# You can customize the settings for each streamer. If not settings were provided, the script would use the streamer_settings from TwitchChannelPointsMiner.
# If no streamer_settings are provided in TwitchChannelPointsMiner the script will use default settings.
# The streamers array can be a String -> username or Streamer instance.

# The settings priority are: settings in mine function, settings in TwitchChannelPointsMiner instance, default settings.
# For example, if in the mine function you don't provide any value for 'make_prediction' but you have set it on TwitchChannelPointsMiner instance, the script will take the value from here.
# If you haven't set any value even in the instance the default one will be used

#twitch_miner.analytics(host="127.0.0.1", port=5000, refresh=5, days_ago=7)   # Start the Analytics web-server

twitch_miner.mine([
    "pokimane", 
    "Emiru", 
    "iGumdrop", 
    "woojungx4", 
    "woohankyung", 
    "sooflower", 
    "aesoon_96", 
    "magenta62", 
    "berry0314", 
    "Corpse_Husband", 
    "irissiri129", 
    "smpk9604", 
    "jo0ju492", 
    "mallang_peach_", 
    "lim1018", 
    "simsul1108", 
    "sonookiii", 
    "sora629", 
    "duswl1214", 
    "darling0416", 
    "bossberry_", 
    "woomewoome", 
    "goyo_0", 
    "saeyobim", 
    "kyul365", 
    "iroiro_o", 
    "momoro9", 
    "yu2bee", 
    "haruzzxng", 
    "rockpuppysing", 
    "gilyoung8", 
    "god_lita", 
    "yomicoskr", 
    "som0322", 
    "maruemon1019", 
    "mozzimanduv", 
    "gyu_0227", 
    "haemingwa", 
    "chodan_", 
    "p_tilda", 
    "haena_0714", 
    "auddk_77", 
    "enako_chan", 
    "yoon_froggy", 
    "we8136", 
    "the_big_cb", 
    "Colas_Bim"
])
