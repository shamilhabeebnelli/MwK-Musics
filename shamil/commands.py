
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters



HOME_TEXT = "<b>Helo, [{}](tg://user?id={})\n\nIam MusicPlayer 2.0 which plays music in Channels and Groups 24*7\n\nI can even Stream Youtube Live in Your Voicechat\n\nDeploy Your Own bot from source code below\n\nHit /help to know about available commands.</b>"
HELP = """

<b>🤖 Read The Below Commands 🤖</b>

**Common Commands**:

**/p**  Reply to an audio file or YouTube link to play it or use /p <song name>.
**/d** Play music from Deezer, Use /d <song name>
**/c**  Show current playing song.
**/help** Show help for commands
**/q** Shows the playlist.

**Admin Commands**:
**/sk** [n] ...  Skip current or n where n >= 2
**/j**  Join voice chat.
**/l**  Leave current voice chat
**/mwk**  Check which VC is joined.
**/sp**  Stop playing.
**/r** Start Radio.
**/sr** Stops Radio Stream.
**/rp**  Play from the beginning.
**/cl** Remove unused RAW PCM files.
**/ps** Pause playing.
**/rs** Resume playing.
**/m**  Mute in VC.
**/um**  Unmute in VC.
**/update** Updates the Bot.
"""



@Client.on_message(filters.command('start'))
async def start(client, message):
    buttons = [
        [
        InlineKeyboardButton('🎭 Developer 🎭️', url='https://t.me/shamilnelli'),
                ],[
                InlineKeyboardButton('🤖 Updates', url='https://t.me/mwklinks'),
                InlineKeyboardButton('🎟️ Movies', url='https://t.me/movieworldkdy'),
                InlineKeyboardButton('📻 Songs', url='https://t.me/mwksongs'),
               ],[
                InlineKeyboardButton('🌎 Source - Code 🌎', url='https://github.com/shamilhabeebnelli/mwk-musics'),
    ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)



@Client.on_message(filters.command("help"))
async def show_help(client, message):
    buttons = [
        [
            InlineKeyboardButton('🎭 Developer 🎭️', url='https://t.me/shamilnelli'),
                ],[
                InlineKeyboardButton('🤖 Updates', url='https://t.me/mwklinks'),
                InlineKeyboardButton('🎟️ Movies', url='https://t.me/movieworldkdy'),
                InlineKeyboardButton('📻 Songs', url='https://t.me/mwksongs'),
               ],[
                InlineKeyboardButton('🌎 Source - Code 🌎', url='https://github.com/shamilhabeebnelli/mwk-musics'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        HELP,
        reply_markup=reply_markup
        )
