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

from pyrogram.handlers import InlineQueryHandler
from youtubesearchpython import VideosSearch
from utils import USERNAME
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultPhoto
from pyrogram import Client, errors
from config import Config
REPLY_MESSAGE=Config.REPLY_MESSAGE
buttons = [
    [
        InlineKeyboardButton("❔ How To Use Me ❔", callback_data="help"),
                ],[
                InlineKeyboardButton('📢 Updates', url='https://t.me/mwklinks'),
                InlineKeyboardButton('💬 Support', url='https://t.me/redbullfed')
                ],[
                InlineKeyboardButton('📜 Source Code 📜', url='https://github.com/shamilhabeebnelli/mwk-musics'),       
    ]
    ]

@Client.on_inline_query()
async def search(client, query):
    answers = []
    if query.query == "KOUTHUKAM_LESHAM_KOODUTHALA":
        answers.append(
            InlineQueryResultPhoto(
                    title="do you wanna help huh?",
                    thumb_url="https://telegra.ph/file/a3937c3ddc19bb3300d89.jpg",
                    photo_url="https://telegra.ph/file/a3937c3ddc19bb3300d89.jpg",
                    caption=(f"{REPLY_MESSAGE}\n\n**Powered By** [ __@MwKLinks | @RedbullFED__ ]"),
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
            )
        await query.answer(results=answers, cache_time=0)
        return
    string = query.query.lower().strip().rstrip()
    if string == "":
        await client.answer_inline_query(
            query.id,
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=("Duration: {} Views: {}").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "/p https://www.youtube.com/watch?v={}".format(
                            v["id"]
                        )
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text=("Nothing found"),
                switch_pm_parameter="",
            )


__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]
