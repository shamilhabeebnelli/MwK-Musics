# Regen & Mod by @shamilhabeebnelli
# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import os
from config import Config
import ffmpeg
from pyrogram import emoji
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR
from pytgcalls import GroupCall
import signal
from pyrogram import Client
from youtube_dl import YoutubeDL
from os import path
bot = Client(
    "MwKVC",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
bot.start()
e=bot.get_me()
USERNAME=e.username

STREAM_URL=Config.STREAM_URL
CHAT=Config.CHAT
GROUP_CALLS = {}
FFMPEG_PROCESSES = {}
RADIO={6}
LOG_GROUP=Config.LOG_GROUP
DURATION_LIMIT=Config.DURATION_LIMIT
playlist=Config.playlist
msg=Config.msg



class MusicPlayer(object):
    def __init__(self):
        self.group_call = GroupCall(path_to_log_file='')
        self.chat_id = None


    

    async def send_text(self, text):
        group_call = self.group_call
        client = group_call.client
        chat_id = LOG_GROUP
        message = await bot.send_message(
            chat_id,
            text,
            disable_web_page_preview=True,
            disable_notification=True
        )
        return message


    async def start_radio(self):
        group_call = mp.group_call
        if group_call.is_connected:
            playlist.clear()   
            group_call.input_filename = ''
            await group_call.stop()
        process = FFMPEG_PROCESSES.get(CHAT)
        if process:
            process.send_signal(signal.SIGTERM)
        station_stream_url = STREAM_URL
        group_call.input_filename = f'radio-{CHAT}.raw'
        try:
            RADIO.remove(0)
        except:
            pass
        try:
            RADIO.add(1)
        except:
            pass
        if os.path.exists(group_call.input_filename):
            os.remove(group_call.input_filename)
        # credits: https://t.me/c/1480232458/6825
        #os.mkfifo(group_call.input_filename)
        process = ffmpeg.input(station_stream_url).output(
            group_call.input_filename,
            format='s16le',
            acodec='pcm_s16le',
            ac=2,
            ar='48k'
        ).overwrite_output().run_async()
        FFMPEG_PROCESSES[CHAT] = process
        while True:
            if os.path.isfile(group_call.input_filename):
                await group_call.start(CHAT)
                break
            else:
                continue

    async def stop_radio(self):
        group_call = mp.group_call
        if group_call:
            playlist.clear()   
            group_call.input_filename = ''
            try:
                RADIO.remove(1)
            except:
                pass
            try:
                RADIO.add(0)
            except:
                pass
        process = FFMPEG_PROCESSES.get(CHAT)
        if process:
            process.send_signal(signal.SIGTERM)

    async def start_call(self):
        group_call = mp.group_call
        await group_call.start(CHAT)
        



mp = MusicPlayer()


# pytgcalls handlers

@mp.group_call.on_network_status_changed
async def network_status_changed_handler(gc: GroupCall, is_connected: bool):
    if is_connected:
        mp.chat_id = int("-100" + str(gc.full_chat.id))
    else:
        mp.chat_id = None


@mp.group_call.on_playout_ended
async def playout_ended_handler(_, __):
    if not playlist:
        await mp.start_radio()
    else:
        await mp.skip_current_playing()
