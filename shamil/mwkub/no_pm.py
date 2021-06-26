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

from pyrogram import Client, filters
from utils import USERNAME
from config import Config
ADMINS=Config.ADMINS
from pyrogram.errors import BotInlineDisabled
@Client.on_message(filters.private & ~filters.bot & filters.incoming)
async def reply(client, message): 
    try:
        inline = await client.get_inline_bot_results(USERNAME, "KOUTHUKAM_LESHAM_KOODUTHALA")
        await client.send_inline_bot_result(
            message.chat.id,
            query_id=inline.query_id,
            result_id=inline.results[0].id,
            hide_via=True
            )
    except BotInlineDisabled:
        for admin in ADMINS:
            try:
                await client.send_message(chat_id=admin, text=f"Hey,\nIt seems you have disabled Inline Mode for @{USERNAME}\n\nA Someone May Be A cyber kozhi or else is spaming me in PM, enable inline mode for @{USERNAME} to reply him")
            except Exception as e:
                print(e)
                pass

    except Exception as e:
        print(e)
        pass
