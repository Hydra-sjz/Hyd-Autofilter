import os
import time
import ffmpeg
import logging
import requests
import youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch

## Extra Fns -------
# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Client.on_message(filters.private & filters.command(['s']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎<b>Sᴇᴀʀᴄʜɪɴɢ ʏᴏᴜʀ sᴏɴɢ</b>...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            channel = results[0]["channel"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return
           
            views = results[0]["views"]
            thumb_name = f'thumb{message.id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Fᴏᴜɴᴅ ɴᴏᴛʜɪɴɢ..Tʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ...🙁')
            return
    except Exception as e:
        m.edit(
            "❎ Found nothing.\n\n𝖯𝗅𝖾𝖺𝗌𝖾 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖮𝗋 𝖲𝖾𝖺𝗋𝖼𝗁 𝖺𝗍 Google.com 𝖥𝗈𝗋 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗈𝖿 𝗍𝗁𝖾 song.\n\nEg.`/s Believer`"
        )
        print(str(e))
        return
    m.edit("📤<b>𝗨ᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ</b>...")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep =  f'🔍<b>Song Dᴏᴡɴʟᴏᴀᴅᴇᴅ</b>\n\n🎙️ <b>ᴛɪᴛʟᴇ:</b> <a href="{link}">{title[:35]}</a>\n⌚ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> `{duration}`\n👁️‍🗨️ <b>ᴠɪᴇᴡs:</b> `{views}`\n🎥 <b>ᴄʜᴀɴɴᴇʟ:</b> {channel}\n\n⚡<i>Youtube Inline Download Powered By Hydrix Tool Bot</i>'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, quote=False, title=title, duration=dur, performer=str(info_dict["uploader"]), thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('`Fᴀɪʟᴅ Tʀʏ Aɢᴀɪɴ Lᴀᴛᴇʀ`')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

