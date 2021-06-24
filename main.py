
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
        await mp.start_radio()

bot.run(main())
bot.start()
@bot.on_message(filters.command("update") & filters.user(Config.ADMINS))
def restart(client, message):
    message.reply_text("Updating Bot...")
    Thread(
        target=stop_and_restart
        ).start()

idle()
bot.stop()
