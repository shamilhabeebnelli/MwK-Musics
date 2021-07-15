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

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, emoji
from utils import mp
from config import Config
playlist=Config.playlist

HELP = """

🎧 <b>I Can Play Music On VoiceChats 🤪</b>

🎶 **Common Commands**:
• `/c`  __Show current playing song__
• `/help` __Show help for commands__
• `/mwk` __Shows the playlist__
• `/stickerid` __To Get Id Of Replied Sticker__

🎶 **Admin Commands**:
• `/p`  __Reply to an audio file or YouTube link to play it or use /p <song name>__
• `/d` __Play music from Deezer, Use /d <song name>__
• `/sk [n]` __...Skip current or n where n >= 2__
• `/j`  __Join voice chat__
• `/l`  __Leave current voice chat__
• `/mwk`  __Check which VC is joined__
• `/sp`  __Stop playing__
• `/r` __Start Radio__
• `/sr` __Stops Radio Stream__
• `/rp`  __Play from the beginning__
• `/cl`  __Remove unused RAW PCM files__
• `/ps` __Pause playing__
• `/rs` __Resume playing__
• `/m`  __Mute in VC__
• `/um`  __Unmute in VC__
• `/update` __Update Current Settings n Restarts the Bot__

© Powered By 
[ __@mwklinks | @redbullfed__ ]
"""



    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton('📢 Updates', url='https://t.me/mwklinks'),
                InlineKeyboardButton('💬 Support', url='https://t.me/redbullfed')
                ],[
                InlineKeyboardButton('🤖 Developer', url='https://t.me/shamilnelli'),
                InlineKeyboardButton('🎧 Songs', url='https://t.me/mwksongs')
                ],[
                InlineKeyboardButton('📜 Source Code 📜', url='https://github.com/shamilhabeebnelli/mwk-musics'),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            HELP,
            reply_markup=reply_markup

        )
