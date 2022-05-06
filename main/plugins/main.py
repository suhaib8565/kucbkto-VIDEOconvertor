#Tg:ChauhanMahesh/Dronebots
#Github.com/vasusen-code

import os
import time
from .. import Drone, LOG_CHANNEL, FORCESUB_UN
from telethon import events, Button
from telethon.tl.types import DocumentAttributeVideo
from main.plugins.rename import media_rename
from main.plugins.compressor import compress, file_compress
from main.plugins.trimmer import trim
from main.plugins.convertor import mp3, flac, wav, mp4, mkv, webm, file, video
from LOCAL.localisation import source_text
from main.plugins.__ import force_sub, db
from ethon.telefunc import fast_download
from ethon.pyfunc import video_metadata

#Don't be a MF by stealing someone's hardwork.
forcesubtext = f"Hey there!To use this bot you've to join @{FORCESUB_UN}.\n\nAlso join @kashir_Bots."

@Drone.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def compin(event):
    if event.is_private:
        media = event.media
        if media:
            yy = await force_sub(event.sender_id)
            if yy is True:
                return await event.reply(forcesubtext)
            banned = await db.is_banned(event.sender_id)
            if banned is True:
                return await event.edit(f'you are Banned to use me!\n\ncontact [SUPPORT]({SUPPORT_LINK})')
            video = event.file.mime_type
            if 'video' in video:
                await event.reply("📽",
                            buttons=[
                                [Button.inline("COMPRESS", data="compress"),
                                 Button.inline("CONVERT", data="convert")],
                                [Button.inline("RENAME", data="rename"),
                                 Button.inline("TRIM", data="trim")]
                            ])
                
            else:
                await event.reply('📦',
                            buttons=[  
                                [Button.inline("RENAME", data="rename")]])

@Drone.on(events.callbackquery.CallbackQuery(data="convert"))
async def convert(event):
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if msg.file.size/1000000 > 1000:
        await event.edit("Free users cannot convert files greater than size 1GB.",
                        buttons=[
                            [Button.inline("PREMIUM.", data="premium")]])
    await event.edit("🔃**CONVERT:**",
                    buttons=[
                        [Button.inline("MP3", data="mp3"),
                         Button.inline("FLAC", data="flac"),
                         Button.inline("WAV", data="wav")],
                        [Button.inline("MP4", data="mp4"),
                         Button.inline("WEBM", data="webm"),
                         Button.inline("MKV", data="mkv")],
                        [Button.inline("FILE", data="file"),
                         Button.inline("VIDEO", data="video")],
                        [Button.inline("BACK", data="back")]])
                        
@Drone.on(events.callbackquery.CallbackQuery(data="back"))
async def back(event):
    await event.edit("📽",
                    buttons=[
                        [Button.inline("COMPRESS", data="compress"),
                         Button.inline("CONVERT", data="convert")],
                        [Button.inline("RENAME", data="rename"),
                         Button.inline("TRIM", data="trim")]])
                            
#-----------------------------------------------------------------------------------------

process1 = []
process2 = []

@Drone.on(events.callbackquery.CallbackQuery(data="premium"))
async def premium(event):
    await event.answer(f'{premium_text}', alert=True)
    
@Drone.on(events.callbackquery.CallbackQuery(data="mp3"))
async def vtmp3(event):
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await mp3(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Another process in progress!")
        
@Drone.on(events.callbackquery.CallbackQuery(data="flac"))
async def vtflac(event):
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await flac(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Another process in progress!")
        
@Drone.on(events.callbackquery.CallbackQuery(data="wav"))
async def vtwav(event):
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await wav(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Another process in progress!")
        
@Drone.on(events.callbackquery.CallbackQuery(data="mp4"))
async def vtmp4(event):
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await mp4(event, msg)
    
@Drone.on(events.callbackquery.CallbackQuery(data="mkv"))
async def vtmkv(event):
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await mkv(event, msg)  
    
@Drone.on(events.callbackquery.CallbackQuery(data="webm"))
async def vtwebm(event):
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await webm(event, msg)  
    
@Drone.on(events.callbackquery.CallbackQuery(data="file"))
async def vtfile(event):
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await file(event, msg)    

@Drone.on(events.callbackquery.CallbackQuery(data="video"))
async def ftvideo(event):
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await video(event, msg)
    
@Drone.on(events.callbackquery.CallbackQuery(data="rename"))
async def rename(event):                            
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        cm = await conv.send_message("Send me a new name for the file as a `reply` to this message.\n\n**NOTE:** `.ext` is not required.")                              
        try:
            m = await conv.get_reply()
            new_name = m.text
            await cm.delete()                    
            if not m:                
                return await cm.edit("No response found.")
        except Exception as e: 
            print(e)
            return await cm.edit("An error occured while waiting for the response.")
    await media_rename(event, msg, new_name)                     
                   
@Drone.on(events.callbackquery.CallbackQuery(data="compress"))
async def compresss(event):
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("compressmedia"):
        await event.delete()
        os.mkdir("compressmedia")
        await compress(event, msg)
        os.rmdir("compressmedia")
    else:
        await event.edit(f"Another process in progress!\n\n**[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**")
    
@Drone.on(events.callbackquery.CallbackQuery(data="trim"))
async def vtrim(event):                            
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    async with Drone.conversation(event.chat_id) as conv: 
        try:
            xx = await conv.send_message("send me the start time of the video you want to trim from as a reply to this. \n\nIn format hh:mm:ss , for eg: `01:20:69` ")
            x = await conv.get_reply()
            st = x.text
            await xx.delete()                    
            if not st:               
                return await xx.edit("No response found.")
        except Exception as e: 
            print(e)
            return await xx.edit("An error occured while waiting for the response.")
        try:
            xy = await conv.send_message("send me the end time of the video you want to trim till as a reply to this.  \n\nIn format hh:mm:ss , for eg: `01:20:69` ")  
            y = await conv.get_reply()
            et = y.text
            await xy.delete()                    
            if not et:                
                return await xy.edit("No response found.")
        except Exception as e: 
            print(e)
            return await xy.edit("An error occured while waiting for the response.")
        await trim(event, msg, st, et)
            
