from aiohttp import ClientSession
from pyrogram import Client, filters
from plugins.function import make_carbon
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
aiohttpsession = ClientSession()

C = "**ᴍᴀᴅᴇ ʙʏ @Htgtoolv4bot**"
F = InlineKeyboardMarkup(
[[
     InlineKeyboardButton("ᴍʏ ɢʀᴏᴜᴘ", url="https://t.me/songdownload_group")
]]
)




@Client.on_message(filters.private & filters.command("carbon"))
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ."
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ."
        )
    user_id = message.from_user.id
    m = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("ᴜᴘʟᴏᴀᴅɪɴɢ..")
    await message.reply_photo(
        photo=carbon,
        caption=C,
        reply_markup=F)
    await m.delete()
    carbon.close()
