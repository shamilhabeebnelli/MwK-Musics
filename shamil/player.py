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
from youtube_dl import YoutubeDL
from config import Config
from pyrogram import Client, filters, emoji
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME, FFMPEG_PROCESSES
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch
from pyrogram import Client
from aiohttp import ClientSession
import signal
import re
U=USERNAME
LOG_GROUP=Config.LOG_GROUP
ADMIN_ONLY=Config.ADMIN_ONLY
DURATION_LIMIT = Config.DURATION_LIMIT
ARQ_API=Config.ARQ_API
session = ClientSession()
arq = ARQ("https://thearq.tech",ARQ_API,session)
playlist=Config.playlist

ADMINS=Config.ADMINS
CHAT=Config.CHAT
LOG_GROUP=Config.LOG_GROUP
playlist=Config.playlist

@Client.on_message(filters.command(["p", f"p@{U}"]) | filters.audio & filters.private)
async def yplay(_, message: Message):
    if ADMIN_ONLY == "Y":
        admins=[749673781]
        grpadmins=await _.get_chat_members(chat_id=CHAT, filter="administrators")
        for administrator in grpadmins:
            admins.append(administrator.user.id)
        if message.from_user.id not in admins:
            await message.reply_sticker("CAACAgUAAxkBAAIJM2DTpi52NSM-O-KnYcC1IzbJos8HAAK6AQACsm0wVffnRbQlKgeTHwQ")
            await message.delete()
            return
    type=""
    yturl=""
    ysearch=""
    if message.audio:
        type="audio"
        m_audio = message
    elif message.reply_to_message and message.reply_to_message.audio:
        type="audio"
        m_audio = message.reply_to_message
    else:
        if message.reply_to_message:
            link=message.reply_to_message.text
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex,link)
            if match:
                type="youtube"
                yturl=message.text
        elif " " in message.text:
            text = message.text.split(" ", 1)
            query = text[1]
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex,query)
            if match:
                type="youtube"
                yturl=query
            else:
                type="query"
                ysearch=query
        else:
            await message.reply_text("You Didn't gave me anything to play. Send me a audio file or reply /p to an audio file.")
            return
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    group_call = mp.group_call
    if type=="audio":
        if round(m_audio.audio.duration / 60) > DURATION_LIMIT:
            await message.reply_text(f"😖 Oops Its Too Lengthy... Permitted Limit is {DURATION_LIMIT} minute(s) this video is {round(m_audio.audio.duration/60)} minute(s)")
            return
        if playlist and playlist[-1][2] \
                == m_audio.audio.file_id:
            await message.reply_text(f"📻 Already added in Que")
            return
        data={1:m_audio.audio.title, 2:m_audio.audio.file_id, 3:"telegram", 4:user}
        playlist.append(data)
        if len(playlist) == 1:
            m_status = await message.reply_text(
                f"📻 Yup Brow Downloading....."
            )
            await mp.download_audio(playlist[0])
            if 1 in RADIO:
                if group_call:
                    group_call.input_filename = ''
                    RADIO.remove(1)
                    RADIO.add(0)
                process = FFMPEG_PROCESSES.get(CHAT)
                if process:
                    process.send_signal(signal.SIGTERM)
            if not group_call.is_connected:
                await mp.start_call()
            file=playlist[0][1]
            group_call.input_filename = os.path.join(
                client.workdir,
                DEFAULT_DOWNLOAD_DIR,
                f"{file}.raw"
            )
            await mp.download_audio(playlist[0])
            if 1 in RADIO:
                if group_call:
                    group_call.input_filename = ''
                    RADIO.remove(1)
                    RADIO.add(0)
                process = FFMPEG_PROCESSES.get(CHAT)
                if process:
                    process.send_signal(signal.SIGTERM)
            if not group_call.is_connected:
                await mp.start_call()
            file=playlist[0][1]
            group_call.input_filename = os.path.join(
                client.workdir,
                DEFAULT_DOWNLOAD_DIR,
                f"{file}.raw"
            )

            await m_status.delete()
            print(f"- START PLAYING: {playlist[0][1]}")
        if not playlist:
            pl = f"📻 Nothing Is On Que"
        else:   
            pl = f"🎧 **Que**:\n" + "\n".join([
                f"**{i}**. **📻{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        if LOG_GROUP and message.chat.id != LOG_GROUP:
            await message.reply_text(pl)
        for track in playlist[:2]:
            await mp.download_audio(track)
        if LOG_GROUP:
            await mp.send_playlist()
        else:
            await message.reply_text(pl)
    if type=="youtube" or type=="query":
        if type=="youtube":
            ytquery=yturl
        elif type=="query":
            ytquery=ysearch
        else:
            return
        msg = await message.reply_text("📻️ **Im On It Bruh...**")
        try:
            results = YoutubeSearch(ytquery, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            ydl_opts = {
                "geo-bypass": True,
                "nocheckcertificate": True
            }
            ydl = YoutubeDL(ydl_opts)
            info = ydl.extract_info(url, False)
            duration = round(info["duration"] / 60)
        except Exception as e:
            await msg.edit(
                "😖 Nothing To Be Found... 👎 Can You Check Spelling"
            )
            print(str(e))
            return
        if int(duration) > DURATION_LIMIT:
            await message.reply_text(f"😖 Oops Its Too Lengthy... Permitted Limit is {DURATION_LIMIT} minute(s) this video is {round(m_audio.audio.duration/60)} minute(s)")
            return

        data={1:title, 2:url, 3:"youtube", 4:user}
        playlist.append(data)
        group_call = mp.group_call
        client = group_call.client
        if len(playlist) == 1:
            m_status = await msg.edit(
                f"📻 Yup Brow Downloading....."
            )
            await mp.download_audio(playlist[0])
            if 1 in RADIO:
                if group_call:
                    group_call.input_filename = ''
                    RADIO.remove(1)
                    RADIO.add(0)
                process = FFMPEG_PROCESSES.get(CHAT)
                if process:
                    process.send_signal(signal.SIGTERM)
            if not group_call.is_connected:
                await mp.start_call()
            file=playlist[0][1]
            group_call.input_filename = os.path.join(
                client.workdir,
                DEFAULT_DOWNLOAD_DIR,
                f"{file}.raw"
            )

            await m_status.delete()
            print(f"- START PLAYING: {playlist[0][1]}")
        else:
            await msg.delete()
        if not playlist:
            pl = f"📻 Nothing Is On Que"
        else:
            pl = f"🎧 **Playlist**:\n" + "\n".join([
                f"**{i}**. **📻️{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        if LOG_GROUP and message.chat.id != LOG_GROUP:
            await message.reply_text(pl)
        for track in playlist[:2]:
            await mp.download_audio(track)
        if LOG_GROUP:
            await mp.send_playlist()
        else:
            await message.reply_text(pl)
    await message.delete()
            
        
   
@Client.on_message(filters.command(["d", f"d@{U}"]))
async def deezer(_, message):
    if ADMIN_ONLY == "Y":
        admins=[749673781]
        grpadmins=await _.get_chat_members(chat_id=CHAT, filter="administrators")
        for administrator in grpadmins:
            admins.append(administrator.user.id)
        if message.from_user.id not in admins:
            await message.reply_sticker("AACAgUAAxkBAAIJM2DTpi52NSM-O-KnYcC1IzbJos8HAAK6AQACsm0wVffnRbQlKgeTHwQ")
            await message.delete()
            return
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if " " in message.text:
        text = message.text.split(" ", 1)
        query = text[1]
    else:
        await message.reply_text("You Didn't gave me anything to play use /d <song name>")
        return
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    group_call = mp.group_call
    msg = await message.reply("📻️ **Downloading From Deezer...**")
    try:
        songs = await arq.deezer(query,1)
        if not songs.ok:
            await msg.edit(songs.result)
            return
        url = songs.result[0].url
        title = songs.result[0].title

    except:
        await msg.edit("😖 Nothing To Be Found... 👎 Can You Check Spelling")
        return
    data={1:title, 2:url, 3:"deezer", 4:user}
    playlist.append(data)
    group_call = mp.group_call
    client = group_call.client
    if len(playlist) == 1:
        m_status = await msg.edit(
            f"📻 Yup Brow Downloading....."
        )
        await mp.download_audio(playlist[0])
        if 1 in RADIO:
            if group_call:
                group_call.input_filename = ''
                RADIO.remove(1)
                RADIO.add(0)
            process = FFMPEG_PROCESSES.get(CHAT)
            if process:
                process.send_signal(signal.SIGTERM)
        if not group_call.is_connected:
            await mp.start_call()
        file=playlist[0][1]
        group_call.input_filename = os.path.join(
            client.workdir,
            DEFAULT_DOWNLOAD_DIR,
            f"{file}.raw"
        )
        await m_status.delete()
        print(f"- START PLAYING: {playlist[0][1]}")
    else:
        await msg.delete()
    if not playlist:
        pl = f"📻 Nothing Is On Que"
    else:
        pl = f"🎧 **Playlist**:\n" + "\n".join([
            f"**{i}**. **📻{x[1]}**\n   👤**Requested by:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
    if LOG_GROUP and message.chat.id != LOG_GROUP:
        await message.reply_text(pl)
    for track in playlist[:2]:
        await mp.download_audio(track)
    if LOG_GROUP:
        await mp.send_playlist()
    else:
        await message.reply_text(pl)
    await message.delete()


@Client.on_message(filters.command(["c", f"c@{U}"]))
async def player(_, m: Message):
    if not playlist:
        await m.reply_text(f"👎 Nothing Is Playing Right Now")
        return
    else:
        pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
            f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
    await m.reply_text(
        pl,
        parse_mode="Markdown",
		reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Replay", callback_data="rp"),
                            InlineKeyboardButton("Pause", callback_data="ps")
                        ],[
                            InlineKeyboardButton("Skip", callback_data="sk"),
                            InlineKeyboardButton("Musics", url="https://t.me/mwksongs")
                ],
			]
			)
    )
    await m.delete()

@Client.on_message(filters.command(["sk", f"sk@{U}"]) & filters.user(ADMINS))
async def skip_track(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply("📻️ Nothing is Playing")
        return
    if len(m.command) == 1:
        await mp.skip_current_playing()
        if not playlist:
            pl = f"📻 Nothing Is On Que"
        else:
            pl = f"🎧 **Playlist**:\n" + "\n".join([
            f"**{i}**. **📻️{x[1]}**\n   👤**Requested by:** {x[4]}"
            for i, x in enumerate(playlist)
            ])            
        if LOG_GROUP and m.chat.id != LOG_GROUP:
            await m.reply_text(pl)
        if LOG_GROUP:
            await mp.send_playlist()
        else:
            await m.reply_text(pl)
    else:
        try:
            items = list(dict.fromkeys(m.command[1:]))
            items = [int(x) for x in items if x.isdigit()]
            items.sort(reverse=True)
            text = []
            for i in items:
                if 2 <= i <= (len(playlist) - 1):
                    audio = f"{playlist[i].audio.title}"
                    playlist.pop(i)
                    text.append(f"{emoji.WASTEBASKET} {i}. **{audio}**")
                else:
                    text.append(f"{emoji.CROSS_MARK} {i}")
            await m.reply_text("\n".join(text))
            if not playlist:
                pl = f"📻 Nothing Is On Que"
            else:
                pl = f"📻️ **Playlist**:\n" + "\n".join([
                    f"**{i}**. **📻️{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(playlist)
                    ])
            if LOG_GROUP and m.chat.id != LOG_GROUP:
                await m.reply_text(pl)
            if LOG_GROUP:
                await mp.send_playlist()
            else:
                await m.reply_text(pl)
        except (ValueError, TypeError):
            await m.reply_text(f"{emoji.NO_ENTRY} Invalid input",
                                       disable_web_page_preview=True)
    await m.delete()

@Client.on_message(filters.command(["join", f"join@{U}"]) & filters.user(ADMINS))
async def join_group_call(client, m: Message):
    group_call = mp.group_call
    if group_call.is_connected:
        await m.reply_text(f"📻 Already joined voice chat")
        return
    await mp.start_call()
    chat = await client.get_chat(CHAT)
    await m.reply_text(f"📻 Succesfully Joined VC in {chat.title}")
    await m.delete()


@Client.on_message(filters.command("l") & filters.user(ADMINS))
async def leave_voice_chat(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Not joined any VC yet.")
        return
    playlist.clear()
    if 1 in RADIO:
        await mp.stop_radio()
    group_call.input_filename = ''
    await group_call.stop()
    await m.reply_text("Left the VC")
    await m.delete()


@Client.on_message(filters.command(["mwk", f"mwk@{U}"]) & filters.user(ADMINS))
async def list_voice_chat(client, m: Message):
    group_call = mp.group_call
    if group_call.is_connected:
        chat_id = int("-100" + str(group_call.full_chat.id))
        chat = await client.get_chat(chat_id)
        await m.reply_text(
            f"📻️ **Currently in the voice chat**:\n"
            f"- **{chat.title}**"
        )
    else:
        await m.reply_text(emoji.NO_ENTRY
                                   + "Didn't join any vc yet")
    await m.delete()


@Client.on_message(filters.command(["sp", f"sp@{U}"]) & filters.user(ADMINS))
async def stop_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Nothing is Playing to Stop.")
        return
    if 1 in RADIO:
        await mp.stop_radio()
    group_call.stop_playout()
    await m.reply_text(f"🤐 Stopped Streaming/Playing")
    playlist.clear()
    await m.delete()

@Client.on_message(filters.command(["rp", f"rp@{U}"]) & filters.user(ADMINS))
async def restart_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Nothing is Playing to Replay.")
        return
    if not playlist:
        await m.reply_text("Empty Playlist.")
        return
    group_call.restart_playout()
    await m.reply_text(
        f"{emoji.COUNTERCLOCKWISE_ARROWS_BUTTON}  "
        "Playing from the beginning..."
    )
    await m.delete()

@Client.on_message(filters.command(["ps", f"ps@{U}"]) & filters.user(ADMINS))
async def pause_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Nothing playing to pause.")
        return
    mp.group_call.pause_playout()
    await m.reply_text(f"⏯ Paused",
                               quote=False)



@Client.on_message(filters.command(["rs", f"rs@{U}"]) & filters.user(ADMINS))
async def resume_playing(_, m: Message):
    if not mp.group_call.is_connected:
        await m.reply_text("Nothing paused to Resume.")
        return
    mp.group_call.resume_playout()
    await m.reply_text(f"⏯ Resumed",
                               quote=False)

@Client.on_message(filters.command(["cl", f"cl@{U}"]) & filters.user(ADMINS))
async def clean_raw_pcm(client, m: Message):
    download_dir = os.path.join(client.workdir, DEFAULT_DOWNLOAD_DIR)
    all_fn: list[str] = os.listdir(download_dir)
    for track in playlist[:2]:
        track_fn = f"{track[1]}.raw"
        if track_fn in all_fn:
            all_fn.remove(track_fn)
    count = 0
    if all_fn:
        for fn in all_fn:
            if fn.endswith(".raw"):
                count += 1
                os.remove(os.path.join(download_dir, fn))
    await m.reply_text(f"{emoji.WASTEBASKET} Cleaned {count} files")
    await m.delete()

@Client.on_message(filters.command(["m", f"m@{U}"]) & filters.user(ADMINS))
async def mute(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Nothing is playing to get muted.")
        return
    group_call.set_is_mute(True)
    await m.reply_text(f"🤐 Muted")
    await m.delete()


@Client.on_message(filters.command(["um", f"um@{U}"]) & filters.user(ADMINS))
async def unmute(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Nothing playing to mute.")
        return
    group_call.set_is_mute(False)
    await m.reply_text(f"🔊 Unmuted")
    await m.delete()

@Client.on_message(filters.command(["q", f"q@{U}"]))
async def show_playlist(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("No active Voicechat.")
        return
    if not playlist:
        pl = f"📻 Nothing Is On Que"
    else:
        pl = f"🎧 **Playlist**:\n" + "\n".join([
            f"**{i}**. **📻️{x[1]}**\n   👤**Requested by:** {x[4]}"
            for i, x in enumerate(play)
            ])
    await m.reply_text(pl)
    await m.delete()

admincmds=["j", "um", "m", "l", "cl", "mwk", "ps", "rs", "sp", "sk", "r", "sr", "rp", "update", f"j@{U}", f"um@{U}", f"m@{U}", f"l@{U}", f"cl@{U}", f"mwk@{U}", f"ps@{U}", f"rs@{U}", f"sp@{U}", f"sk@{U}", f"r@{U}", f"sr@{U}", f"rp@{U}", f"update@{U}"]

@Client.on_message(filters.command(admincmds) & ~filters.user(ADMINS))
async def notforu(_, m: Message):
    await.message.reply_sticker("CAACAgUAAxkBAAIJM2DTpi52NSM-O-KnYcC1IzbJos8HAAK6AQACsm0wVffnRbQlKgeTHwQ")
