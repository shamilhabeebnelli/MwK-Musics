
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters



HOME_TEXT = "<b>Helo, [{}](tg://user?id={})\n\n• Iam A Bot Project by MwK MusicS\n• I Can Manage Group VC's\n\n• Hit /help to know about available commands.</b>"
HELP = """
🎧 <b>I Can Play Musics On VoiceChats 🤪</b>

🎶 **Common Commands**:
• `/song` __Download Song from youtube__
• `/c`  __Show current playing song__
• `/help` __Show help for commands__
• `/mwk` __Shows the playlist__

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



@Client.on_message(filters.command('start'))
async def start(client, message):
    buttons = [
        [
        InlineKeyboardButton("❔ How To Use Me ❔", callback_data="help"),
                ],[
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
    await message.reply_photo(photo="https://telegra.ph/file/a3937c3ddc19bb3300d89.jpg", caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)



@Client.on_message(filters.command("help"))
async def show_help(client, message):
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
    await message.reply_photo(photo="https://telegra.ph/file/a3937c3ddc19bb3300d89.jpg", caption=HELP, reply_markup=reply_markup)
