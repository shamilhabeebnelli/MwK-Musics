# A Subinps Project
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
• `/current`  __Show current playing song__
• `/help` __Show help for commands__
• `/mwk` __Shows the playlist__
• `/stickerid` __To Get Id Of Replied Sticker__

🎶 **Admin Commands**:
• `/play`  __Reply to an audio file or YouTube link to play it or use /p <song name>__
• `/dplay` __Play music from Deezer, Use /d <song name>__
• `/skip [n]` __...Skip current or n where n >= 2__
• `/join`  __Join voice chat__
• `/leave`  __Leave current voice chat__
• `/mwk`  __Check which VC is joined__
• `/stop`  __Stop playing__
• `/radio` __Start Radio__
• `/stopradio` __Stops Radio Stream__
• `/replay`  __Play from the beginning__
• `/clear`  __Remove unused RAW PCM files__
• `/pause` __Pause playing__
• `/resume` __Resume playing__
• `/mute`  __Mute in VC__
• `/unmute`  __Unmute in VC__
• `/update` __Update Current Settings n Restarts the Bot__

© Powered By 
[ __@mwkBoTs | @subin_works__ ]
"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "rp":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"😖 Nothing On Que Ser"
        else:
            pl = f"🎧 **Playlist**:\n" + "\n".join([
                f"**{i}**. **📻{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(
                f"{pl}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Replay", callback_data="rp"),
                            InlineKeyboardButton("Pause", callback_data="ps")
                        ],[
                            InlineKeyboardButton("Skip", callback_data="sk"),
                            InlineKeyboardButton("Report Bug", url="subinps_bot")
                        ]
                    ]
                )
            )

    elif query.data == "ps":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            pl = f"🎧 **Playlist**:\n" + "\n".join([
                f"**{i}**. **📻{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Paused\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Replay", callback_data="replace"),
                            InlineKeyboardButton("Resume", callback_data="resume")
                        ],[
                            InlineKeyboardButton("Skip", callback_data="skip"),
                            InlineKeyboardButton("Updates", url='t.me/mwkBoTs')
                        ],
                    ]
                )
            )

    
    elif query.data == "rs":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            pl = f"🎧 **Playlist**:\n" + "\n".join([
                f"**{i}**. **📻{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Resumed\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Replay", callback_data="rp"),
                            InlineKeyboardButton("Pause", callback_data="ps")
                        ],[
                            InlineKeyboardButton("Skip", callback_data="sk"),
                            InlineKeyboardButton("Support", url="https://t.me/redbullfed") 
                        ],
                    ]
                )
            )

    elif query.data=="sk":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            pl = f"🎧 **Playlist**:\n" + "\n".join([
                f"**{i}**. **📻{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Skipped\n\n{pl}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Replay", callback_data="rp"),
                            InlineKeyboardButton("Pause", callback_data="ps")
                        ],[
                            InlineKeyboardButton("Skip", callback_data="sk"),
                            InlineKeyboardButton("Updates", url="t.me/subin_works")
                            
                    ],
                ]
            )
        )
        except:
            pass
    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton('📢 Updates', url='https://t.me/mwklinks'),
                InlineKeyboardButton('💬 Support', url='https://t.me/redbullfed')
                ],[
                InlineKeyboardButton('🤖 Developer', url='t.me/subinps'),
                InlineKeyboardButton('Bugs', url='t.me/subin_works')
                ],[
                InlineKeyboardButton('📜 Source Code 📜', url='https://github.com/shamilhabeebnelli/mwk-musics'),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            HELP,
            reply_markup=reply_markup

        )
