
from pyrogram import Client, idle, filters
import os
from threading import Thread
import sys
from config import Config
from utils import mp
import asyncio
from pyrogram.raw import functions, types


CHAT=Config.CHAT
bot = Client(
    "MwkVC",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="shamil")
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")
async def main():
    async with bot:
        await mp.startupradio()
        await asyncio.sleep(2)
        await mp.startupradio()

def stop_and_restart():
        bot.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)
    
bot.run(main())
bot.start()
bot.send(
    functions.bots.SetBotCommands(
        commands=[
            types.BotCommand(
                command="start",
                description="Check if bot alive"
            ),
            types.BotCommand(
                command="help",
                description="Shows help message"
            ),
            types.BotCommand(
                command="p",
                description="Play song from youtube/audiofile"
            ),
            types.BotCommand(
                command="d",
                description="Play song from Deezer"
            ),
            types.BotCommand(
                command="c",
                description="Shows current playing song with controls"
            ),
            types.BotCommand(
                command="q",
                description="Shows the playlist"
            ),
            types.BotCommand(
                command="sk",
                description="Skip the current song"
            ),
            types.BotCommand(
                command="j",
                description="Join VC"
            ),
            types.BotCommand(
                command="l",
                description="Leave from VC"
            ),
            types.BotCommand(
                command="mwk",
                description="Ckeck if VC is joined"
            ),
            types.BotCommand(
                command="sp",
                description="Stops Playing"
            ),
            types.BotCommand(
                command="r",
                description="Start radio / Live stream"
            ),
            types.BotCommand(
                command="sr",
                description="Stops radio/Livestream"
            ),
            types.BotCommand(
                command="rp",
                description="Replay from beggining"
            ),
            types.BotCommand(
                command="cl",
                description="Cleans RAW files"
            ),
            types.BotCommand(
                command="ps",
                description="Pause the song"
            ),
            types.BotCommand(
                command="rs",
                description="Resume the paused song"
            ),
            types.BotCommand(
                command="m",
                description="Mute in VC"
            ),
            types.BotCommand(
                command="um",
                description="Unmute in VC"
            ),
            types.BotCommand(
                command="source",
                description="source code"
            ),
            types.BotCommand(
                command="update",
                description="Restart the bot"
            )
        ]
    )
)


@bot.on_message(filters.command("update") & filters.user(Config.ADMINS))
def restart(client, message):
    message.reply_text("Updating Bot...")
    Thread(
        target=stop_and_restart
        ).start()

idle()
bot.stop()
