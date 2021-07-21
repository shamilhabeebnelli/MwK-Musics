from config import Config
from pyrogram import Client
from config import Config
    USER = Client(
        Config.SESSION,
        Config.API_ID,
        Config.API_HASH,
        plugins=dict(root="shamil.mwkub")
        )
else:
    USER = Client(
        Config.SESSION,
        Config.API_ID,
        Config.API_HASH
        )
USER.start()
