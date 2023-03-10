from __future__ import unicode_literals

import asyncio
import math
import os
import time
from random import randint
from urllib.parse import urlparse

import aiofiles
import aiohttp
import requests
import wget
import yt_dlp
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.decorators import humanbytes




ydl_opts = {
    'format': 'best',
    'keepvideo': True,
    'prefer_ffmpeg': False,
    'geo_bypass': True,
    'outtmpl': '%(title)s.%(ext)s',
    'quite': True
}





#JIOSAAVN-DL
@Client.on_message(filters.private & filters.command(["saavn"]))
def song(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("ð `Searching your file in JioSaavn...`")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        duration = results[0]["duration"]
        views = results[0]["views"]
        channel = results[0]["channel"]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit(f"`Hi {message.from_user.first_name} your given wrong command arguments`â¼ï¸â¼ï¸\n\n`á´ðð¾ðºðð¾ É¢Éªá´ á´ á´á´ á´ á´ á´ÊÉªá´ sá´É´É¢ É´á´á´á´ á´ð Go Jiosaavn.com and find your favourite song, and copy the song name some example downbelow.`\n\n**Example:**\n- `/saavn dilbar`\n- `/saavn de taali`")
        print(str(e))
        return
    m.edit("[ð¶](https://telegra.ph/file/bff0e94ded0ae083ea7fd.jpg)`Prosessing your song file from JioSaavn`\nâ³`Please wait for some time`")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**Jio Saavn**\nð **Title:** [{title[:50]}](https://www.jiosaavn.com)\nâ±ï¸ **Duration:** `{duration}`\n\nâï¸__Jio Saavn Song Download Powered By á´á´sÉªá´âá´Ê__"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("**Jio Saavn**\n[ðµ](https://telegra.ph/file/bff0e94ded0ae083ea7fd.jpg)`Your requested song is Uploading...`\n`Please wait...`")
        message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            title=title,
            duration=dur,
            reply_markup=InlineKeyboardMarkup( [[
             InlineKeyboardButton(f"Uploaded by: ÊÊá´ÊÉªx Êá´á´", url="https://t.me/Htgtoolv4bot")
             ]]
            )
        )
        m.delete()
    except Exception as e:
        m.edit("`Fá´á´É´á´ É´á´á´ÊÉªÉ´É¢...á´É´ IÉ´á´á´ÊÉ´á´Ê á´ÊÊá´Ê á´á´á´á´Êá´á´. á´ÊÊ á´É¢á´ÉªÉ´ Êá´á´á´Ê...`")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
