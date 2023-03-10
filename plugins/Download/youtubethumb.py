import os
import time
import ytthumb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from youtube_search import YoutubeSearch


@Client.on_message(filters.private & filters.command(["ytthumb", 'dlthumb']))
async def send_thumbnail(bot, update):
    message = await update.reply_text(
        text="`Analysing...`",
        disable_web_page_preview=True,
        quote=True
    )
    try:
        if " | " in update.text:
            video = update.text.split(" | ", -1)[0]
            quality = update.text.split(" | ", -1)[1]
        else:
            video = update.text
            quality = "sd"
        thumbnail = ytthumb.thumbnail(
            video=video,
            quality=quality
        )
        await update.reply_photo(
            photo=thumbnail,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('ᴍʏ ɢʀᴏᴜᴘ', url='https://t.me/Music_Galaxy_Dl')]]),
            quote=True
        )
        await message.delete()
    except Exception as error:
        await message.edit_text(
            text="**Please Use** /ytthumb (youtube link)\n\n**Example:** `/ytthumb http://www.youtube.com/watch?v=HhjHYkPQ8F0`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('ᴍʏ ɢʀᴏᴜᴘ', url='https://t.me/Music_Galaxy_Dl')]])
        )
