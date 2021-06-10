
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import mp, RADIO
from config import Config
from config import STREAM

ADMINS=Config.ADMINS

@Client.on_message(filters.command("r") & filters.user(ADMINS))
async def radio(client, message: Message):
    if 1 in RADIO:
        await message.reply_text("Kindly stop existing Stream /sr")
        return
    await mp.start_radio()
    await message.reply_text(f"Started Streaming: <code>{STREAM}</code>")

@Client.on_message(filters.command('sr') & filters.user(ADMINS))
async def stop(_, message: Message):
    if 0 in RADIO:
        await message.reply_text("Kindly Start Streaming First /r")
        return
    await mp.stop_radio()
    await message.reply_text("Radio stream ended.")
