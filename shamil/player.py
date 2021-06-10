
import os
from config import Config
from pyrogram import Client, filters, emoji
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR
from pyrogram.types import Message
from utils import mp, RADIO
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch
from pyrogram import Client
from aiohttp import ClientSession
import re

LOG_GROUP=Config.LOG_GROUP

DURATION_LIMIT = Config.DURATION_LIMIT
ARQ_API=Config.ARQ_API
session = ClientSession()
arq = ARQ("https://thearq.tech",ARQ_API,session)
playlist=Config.playlist

ADMINS=Config.ADMINS
CHAT=Config.CHAT
LOG_GROUP=Config.LOG_GROUP
playlist=Config.playlist

@Client.on_message(filters.command("p") | filters.audio & filters.private)
async def yplay(_, message: Message):
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
    if 1 in RADIO:
        await mp.stop_radio()
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    group_call = mp.group_call
    if not group_call.is_connected:
        await mp.start_call()
    if type=="audio":
        if round(m_audio.audio.duration / 60) > DURATION_LIMIT:
            await message.reply_text(f"😖 Oops Its Too Lengthy... Permitted Limit is {DURATION_LIMIT} minute(s)")
            return
        if not group_call.is_connected:
            await mp.start_call()
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
            file=playlist[0][1]
            group_call.input_filename = os.path.join(
                _.workdir,
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
        await message.reply_text(pl)
        for track in playlist[:2]:
            await mp.download_audio(track)
        if LOG_GROUP and message.chat.id != LOG_GROUP:
            await mp.send_playlist()
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
            duration = results[0]["duration"]
        except Exception as e:
            await msg.edit(
                "😖 Nothing To Be Found... 👎 Can You Check Spelling "
            )
            print(str(e))
            return
        if duration > DURATION_LIMIT:
            await message.reply_text(f"😖 Oops Its Too Lengthy... Permitted Limit is {DURATION_LIMIT} minute(s)")
            return

        data={1:title, 2:url, 3:"youtube", 4:user}
        playlist.append(data)
        group_call = mp.group_call
        if not group_call.is_connected:
            await mp.start_call()
        client = group_call.client
        if len(playlist) == 1:
            m_status = await msg.edit(
                f"📻 Yup Brow Downloading....."
            )
            await mp.download_audio(playlist[0])
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
            pl = f"🎧 **Playlist**:\n" + "\n".join([
                f"**{i}**. **📻️{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await message.reply_text(pl)
        for track in playlist[:2]:
            await mp.download_audio(track)
        if LOG_GROUP and message.chat.id != LOG_GROUP:
            await mp.send_playlist()
            
        
   
@Client.on_message(filters.command("d"))
async def deezer(_, message):
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if " " in message.text:
        text = message.text.split(" ", 1)
        query = text[1]
    else:
        await message.reply_text("You Didn't gave me anything to play use /d <song name>")
        return
    if 1 in RADIO:
        await mp.stop_radio()
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    group_call = mp.group_call
    if not group_call.is_connected:
        await mp.start_call()
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
    if not group_call.is_connected:
        await mp.start_call()
    client = group_call.client
    if len(playlist) == 1:
        m_status = await msg.edit(
            f"📻 Yup Brow Downloading..... And Processing...."
        )
        await mp.download_audio(playlist[0])
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
        pl = f"🎧 **Playlist**:\n" + "\n".join([
            f"**{i}**. **📻{x[1]}**\n   👤**Requested by:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
    await message.reply_text(pl)
    for track in playlist[:2]:
        await mp.download_audio(track)
    if LOG_GROUP and message.chat.id != LOG_GROUP:
        await mp.send_playlist()


@Client.on_message(filters.command("c"))
async def player(_, m: Message):
    if not playlist:
        await m.reply_text(f"📻 Nothing Is On Que")
        return
    else:
        pl = f"🎧 **Playlist**:\n" + "\n".join([
            f"**{i}**. **📻️{x[1]}**\n   👤**Requested by:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
    await m.reply_text(
        pl,
        parse_mode="Markdown",
		reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔄 Replay", callback_data="rp"),
                            InlineKeyboardButton("⏯ Pause", callback_data="ps")
                        ],[
                            InlineKeyboardButton("⏩ Skip", callback_data="sk"),
                            InlineKeyboardButton("📻 Musics", url="https://t.me/mwksongs")
                ],
			]
			)
    )

@Client.on_message(filters.command("sk") & filters.user(ADMINS))
async def skip_track(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply("📻 Nothing Is Playing")
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
        await m.reply_text(pl)
        if LOG_GROUP and m.chat.id != LOG_GROUP:
            await mp.send_playlist()
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
            await m.reply_text(pl)
            if LOG_GROUP and m.chat.id != LOG_GROUP:
                await mp.send_playlist()
        except (ValueError, TypeError):
            await m.reply_text(f"🤐 Invalid input",
                                       disable_web_page_preview=True)


@Client.on_message(filters.command("j") & filters.user(ADMINS))
async def join_group_call(client, m: Message):
    group_call = mp.group_call
    if group_call.is_connected:
        await m.reply_text(f"📻 Already joined voice chat")
        return
    await mp.start_call()
    chat = await client.get_chat(CHAT)
    await m.reply_text(f"📻 Succesfully Joined VC in {chat.title}")


@Client.on_message(filters.command("l") & filters.user(ADMINS))
async def leave_voice_chat(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Not joined any VC yet.")
        return
    playlist.clear()
    group_call.input_filename = ''
    await group_call.stop()
    await m.reply_text("Left the VC")


@Client.on_message(filters.command("mwk") & filters.user(ADMINS))
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
                                   + "Didn't join any voice chat yet")


@Client.on_message(filters.command("sp") & filters.user(ADMINS))
async def stop_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Nothing is Playing to Stop.")
        return
    group_call.stop_playout()
    await m.reply_text(f"🤐 Stopped Streaming/Playing")
    playlist.clear()


@Client.on_message(filters.command("rp") & filters.user(ADMINS))
async def restart_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Nothing is Playing to Replay.")
        return
    if not playlist:
        return
    group_call.restart_playout()
    await m.reply_text(
        f"{emoji.COUNTERCLOCKWISE_ARROWS_BUTTON}  "
        "Playing from the beginning..."
    )


@Client.on_message(filters.command("ps") & filters.user(ADMINS))
async def pause_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Nothing playing to pause.")
        return
    mp.group_call.pause_playout()
    await m.reply_text(f"⏯ Paused",
                               quote=False)



@Client.on_message(filters.command("rs") & filters.user(ADMINS))
async def resume_playing(_, m: Message):
    if not mp.group_call.is_connected:
        await m.reply_text("Nothing paused to Resume.")
        return
    mp.group_call.resume_playout()
    await m.reply_text(f"⏯ Resumed",
                               quote=False)

@Client.on_message(filters.command("cl") & filters.user(ADMINS))
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
    await m.reply_text(f"{emoji.WASTEBASKET} Cleaned {count} Files Succesfully")


@Client.on_message(filters.command("m") & filters.user(ADMINS))
async def mute(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Nothing playing to mute.")
        return
    group_call.set_is_mute(True)
    await m.reply_text(f"🤐 Muted")


@Client.on_message(filters.command("um") & filters.user(ADMINS))
async def unmute(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("Nothing is playing to unmute.")
        return
    group_call.set_is_mute(False)
    await m.reply_text(f"🔊 Unmuted")

@Client.on_message(filters.command("C"))
async def show_playlist(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        await m.reply_text("There is no Active VC.")
        return
    if not playlist:
        pl = f"📻 Nothing Is On Que"
    else:
        pl = f"🎧 **Playlist**:\n" + "\n".join([
            f"**{i}**. **📻️{x[1]}**\n   👤**Requested by:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
    await m.reply_text(pl)

admincmds=["j", "um", "m", "l", "cl", "mwk", "ps", "rs", "sp", "sk", "r", "sr", "rp", "update"]

@Client.on_message(filters.command(admincmds) & ~filters.user(ADMINS))
async def notforu(_, m: Message):
    await m.reply("Go Away Stupid 🤣")
