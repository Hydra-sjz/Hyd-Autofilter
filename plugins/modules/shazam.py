import os
import asyncio
from shazamio import Shazam
from plugins.humanbyte import humanbytes
from pyrogram import filters, Client
import datetime
import requests
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.cmd import edit_or_reply, runcmd, fetch_audio








@Client.on_message(filters.private & filters.command(["audify"]))
async def shazamm(client, message):
    rsr1 = await edit_or_reply(message, "โณ")
    if not message.reply_to_message:
        await rsr1.edit("Reply Audio or Video.")
        return
    if os.path.exists("friday.mp3"):
        os.remove("friday.mp3")
    kkk = await fetch_audio(client, message)
    downloaded_file_name = kkk
    f = {"file": (downloaded_file_name, open(downloaded_file_name, "rb"))}
    await rsr1.edit("๐")
    r = requests.post("https://starkapi.herokuapp.com/shazam/", files=f)
    try:
        xo = r.json()
    except JSONDecodeError:
        await rsr1.edit("**Song not found๐**")
        return
    if xo.get("success") is False:
        await rsr1.edit("**Song not found๐**")
        os.remove(downloaded_file_name)
        return
    xoo = xo.get("response")
    zz = xoo[1]
    zzz = zz.get("track")
    if not zzz:
        await rsr1.edit("**Song not found๐**")
        return
    nt = zzz.get("images")
    image = nt.get("coverarthq")
    by = zzz.get("subtitle")
    title = zzz.get("title")
    messageo = f"""<b><u>Identify Finished โ</b></u>\n
<b>๐ Song Name : </b> {title}\n
<b>๐๏ธ Artist : </b>{by}
"""
    await client.send_photo(message.chat.id, image, messageo, reply_to_message_id=message.reply_to_message.id, parse_mode="HTML")
    os.remove(downloaded_file_name)
    await rsr1.delete()

	
