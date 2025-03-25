#telegram username: @Shidoteshika1

import random
from bot import Bot
from plugins.FORMATS import *
from config import OWNER_ID, PICS
from plugins.advance_features import convert_time
from database.database import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
    
async def fileSettings(getfunc, setfunc=None, delfunc=False) :
    btn_mode, txt_mode, pic_mode = '❌', off_txt, off_pic
    del_btn_mode = 'Eɴᴀʙʟᴇ Mᴏᴅᴇ ✅'
    try:
        if not setfunc:
            if await getfunc():
                txt_mode = on_txt    
                btn_mode = '✅'
                del_btn_mode = 'Dɪsᴀʙʟᴇ Mᴏᴅᴇ ❌'
        
            return txt_mode, (del_btn_mode if delfunc else btn_mode)
            
        else:
            if await getfunc():
                await setfunc(False)
            else:
                await setfunc(True)
                pic_mode, txt_mode = on_pic, on_txt
                btn_mode = '✅'
                del_btn_mode = 'Dɪsᴀʙʟᴇ Mᴏᴅᴇ ❌'
                
            return pic_mode, txt_mode, (del_btn_mode if delfunc else btn_mode)
            
    except Exception as e:
        print(f"Error occured at [fileSettings(getfunc, setfunc=None, delfunc=False)] : {e}")

def buttonStatus(pc_data: str, hc_data: str, cb_data: str) -> list:
    button = [
        [
            InlineKeyboardButton(f'Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ: {pc_data}', callback_data='pc'),
            InlineKeyboardButton(f'Hɪᴅᴇ Cᴀᴘᴛɪᴏɴ: {hc_data}', callback_data='hc')
        ],
        [
            InlineKeyboardButton(f'Cʜᴀɴɴᴇʟ Bᴜᴛᴛᴏɴ: {cb_data}', callback_data='cb'), 
            InlineKeyboardButton(f'◈ Sᴇᴛ Bᴜᴛᴛᴏɴ ➪', callback_data='setcb')
        ],
        [
            InlineKeyboardButton('🔄 Rᴇғʀᴇsʜ', callback_data='files_cmd'), 
            InlineKeyboardButton('Cʟᴏsᴇ ✖️', callback_data='close')
        ],
    ]
    return button

#functin help to checking if a user is admin or owner before processing query....
async def authoUser(query, user_id, owner_only=False):
    if not owner_only:
        if not any([user_id == OWNER_ID, await admin_exist(user_id)]):
            await query.answer("❌ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ Aᴅᴍɪɴ !", show_alert=True)
            return False
    else:
        if user_id != OWNER_ID:
            await query.answer("❌ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ Oᴡɴᴇʀ !", show_alert=True)
            return False
        
    await query.answer("♻️ Qᴜᴇʀʏ Pʀᴏᴄᴇssɪɴɢ....") 
    return True   

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data        
    if data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
            
    elif data == "about":
        user = await client.get_users(OWNER_ID)
        user_link = f"https://t.me/{user.username}" if user.username else f"tg://openmessage?user_id={OWNER_ID}" 
        ownername = f"<a href={user_link}>{user.first_name}</a>" if user.first_name else f"<a href={user_link}>no name !</a>"
        await query.edit_message_media(
            InputMediaPhoto("https://telegra.ph/file/ff8fbe7d67a3c7492c353.jpg", 
                            ABOUT_TXT.format(
                                botname = client.name,
                                ownername = ownername, 
                            )
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('⬅️ Bᴀᴄᴋ', callback_data='start'), InlineKeyboardButton('Cʟᴏsᴇ ✖️', callback_data='close')]
            ]),
        )
        
    elif data == "setting":
        await query.edit_message_media(InputMediaPhoto(random.choice(PICS), "<b>Pʟᴇᴀsᴇ wᴀɪᴛ !\n\n<i>🔄 Rᴇᴛʀɪᴇᴠɪɴɢ ᴀʟʟ Sᴇᴛᴛɪɴɢs...</i></b>"))
        try:
            total_fsub = len(await get_all_channels())
            total_admin = len(await get_all_admins())
            total_ban = len(await get_ban_users())
            autodel_mode = 'Eɴᴀʙʟᴇᴅ' if await get_auto_delete() else 'Dɪsᴀʙʟᴇᴅ'
            protect_content = 'Eɴᴀʙʟᴇᴅ' if await get_protect_content() else 'Dɪsᴀʙʟᴇᴅ'
            hide_caption = 'Eɴᴀʙʟᴇᴅ' if await get_hide_caption() else 'Dɪsᴀʙʟᴇᴅ'
            chnl_butn = 'Eɴᴀʙʟᴇᴅ' if await get_channel_button() else 'Dɪsᴀʙʟᴇᴅ'
            
            await query.edit_message_media(
                InputMediaPhoto(random.choice(PICS),
                                SETTING_TXT.format(
                                    total_fsub = total_fsub,
                                    total_admin = total_admin,
                                    total_ban = total_ban,
                                    autodel_mode = autodel_mode,
                                    protect_content = protect_content,
                                    hide_caption = hide_caption,
                                    chnl_butn = chnl_butn
                                )
                ),
                reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('⬅️ Bᴀᴄᴋ', callback_data='start'), InlineKeyboardButton('Cʟᴏsᴇ ✖️', callback_data='close')]
                ]),
            )
        except Exception as e:
            print(f"! Error Occured on callback data = 'setting' : {e}")
        
    elif data == "start":
        await query.edit_message_media(
            InputMediaPhoto(random.choice(PICS), 
                            START_MSG.format(
                                first = query.from_user.first_name,
                                last = query.from_user.last_name,
                                username = None if not query.from_user.username else '@' + query.from_user.username,
                                mention = query.from_user.mention,
                                id = query.from_user.id
                            )
            ),
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('🤖 Aʙᴏᴜᴛ ᴍᴇ', callback_data='about'), InlineKeyboardButton('Sᴇᴛᴛɪɴɢs ⚙️', callback_data='setting')]
            ]),
        )
        
    elif data == "files_cmd":
        if await authoUser(query, query.from_user.id):   
            try:
                protect_content, pcd = await fileSettings(get_protect_content)
                hide_caption, hcd = await fileSettings(get_hide_caption)
                channel_button, cbd = await fileSettings(get_channel_button)
                name, link = await get_channel_button_link()
                
                await query.edit_message_media(
                    InputMediaPhoto(files_cmd_pic,
                                    FILES_CMD_TXT.format(
                                        protect_content = protect_content,
                                        hide_caption = hide_caption,
                                        channel_button = channel_button,
                                        name = name,
                                        link = link
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup(buttonStatus(pcd, hcd, cbd)),
                )                   
            except Exception as e:
                print(f"! Error Occured on callback data = 'files_cmd' : {e}")
            
    elif data == "pc":
        if await authoUser(query, query.from_user.id):   
            try:
                pic, protect_content, pcd = await fileSettings(get_protect_content, set_protect_content)
                hide_caption, hcd = await fileSettings(get_hide_caption)   
                channel_button, cbd = await fileSettings(get_channel_button) 
                name, link = await get_channel_button_link()
                
                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    FILES_CMD_TXT.format(
                                        protect_content = protect_content,
                                        hide_caption = hide_caption,
                                        channel_button = channel_button,
                                        name = name,
                                        link = link
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup(buttonStatus(pcd, hcd, cbd))
                )                   
            except Exception as e:
                print(f"! Error Occured on callback data = 'pc' : {e}")
            
    elif data == "hc":
        if await authoUser(query, query.from_user.id):     
            try:
                protect_content, pcd = await fileSettings(get_protect_content)
                pic, hide_caption, hcd = await fileSettings(get_hide_caption, set_hide_caption)   
                channel_button, cbd = await fileSettings(get_channel_button) 
                name, link = await get_channel_button_link()
                
                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    FILES_CMD_TXT.format(
                                        protect_content = protect_content,
                                        hide_caption = hide_caption,
                                        channel_button = channel_button,
                                        name = name,
                                        link = link
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup(buttonStatus(pcd, hcd, cbd))
                )                   
            except Exception as e:
                print(f"! Error Occured on callback data = 'hc' : {e}")
            
    elif data == "cb":
        if await authoUser(query, query.from_user.id):   
            try:
                protect_content, pcd = await fileSettings(get_protect_content)
                hide_caption, hcd = await fileSettings(get_hide_caption)   
                pic, channel_button, cbd = await fileSettings(get_channel_button, set_channel_button) 
                name, link = await get_channel_button_link()
                
                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    FILES_CMD_TXT.format(
                                        protect_content = protect_content,
                                        hide_caption = hide_caption,
                                        channel_button = channel_button,
                                        name = name,
                                        link = link
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup(buttonStatus(pcd, hcd, cbd))
                )                   
            except Exception as e:
                print(f"! Error Occured on callback data = 'cb' : {e}")
            
    elif data == "setcb":
        id = query.from_user.id
        if await authoUser(query, id):   
            try:
                button_name, button_link = await get_channel_button_link()
            
                button_preview = [[InlineKeyboardButton(text=button_name, url=button_link)]]  
                set_msg = await client.ask(chat_id = id, text=f'<b>Tᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴ, Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛs ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ.\nFᴏʀ ᴇxᴀᴍᴘʟᴇ:\n<blockquote><code>Join Channel - https://t.me/btth480p</code></blockquote>\n\n<i>Bᴇʟᴏᴡ ɪs ʙᴜᴛᴛᴏɴ Pʀᴇᴠɪᴇᴡ ⬇️</i></b>', timeout=60, reply_markup=InlineKeyboardMarkup(button_preview), disable_web_page_preview = True)
                button = set_msg.text.split(' - ')
                
                if len(button) != 2:
                    markup = [[InlineKeyboardButton(f'◈ Sᴇᴛ Cʜᴀɴɴᴇʟ Bᴜᴛᴛᴏɴ ➪', callback_data='setcb')]]
                    return await set_msg.reply("<b>Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛs.\nFᴏʀ ᴇxᴀᴍᴘʟᴇ:\n<blockquote><code>Join Channel - https://t.me/btth480p</code></blockquote>\n\n<i>Tʀʏ ᴀɢᴀɪɴ ʙʏ ᴄʟɪᴄᴋɪɴɢ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ..</i></b>", reply_markup=InlineKeyboardMarkup(markup), disable_web_page_preview = True)
                
                button_name = button[0].strip(); button_link = button[1].strip()
                button_preview = [[InlineKeyboardButton(text=button_name, url=button_link)]]
                
                await set_msg.reply("<b><i>Aᴅᴅᴇᴅ Sᴜᴄcᴇssғᴜʟʟʏ ✅</i>\n<blockquote>Sᴇᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴀs Pʀᴇᴠɪᴇᴡ ⬇️</blockquote></b>", reply_markup=InlineKeyboardMarkup(button_preview))
                await set_channel_button_link(button_name, button_link)
                return
            except Exception as e:
                try:
                    await set_msg.reply(f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")
                    print(f"! Error Occured on callback data = 'setcb' : {e}")
                except:
                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                    print(f"! Error Occured on callback data = 'setcb' -> Rᴇᴀsᴏɴ: 1 minute Time out ..")

    elif data == 'autodel_cmd':
        if await authoUser(query, query.from_user.id, owner_only=True):            
            try:
                timer = convert_time(await get_del_timer())
                autodel_mode, mode = await fileSettings(get_auto_delete, delfunc=True)
                
                await query.edit_message_media(
                    InputMediaPhoto(autodel_cmd_pic,
                                    AUTODEL_CMD_TXT.format(
                                        autodel_mode = autodel_mode,
                                        timer = timer
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton(mode, callback_data='chng_autodel'), InlineKeyboardButton('◈ Sᴇᴛ Tɪᴍᴇʀ ⏱', callback_data='set_timer')],
                        [InlineKeyboardButton('🔄 Rᴇғʀᴇsʜ', callback_data='autodel_cmd'), InlineKeyboardButton('Cʟᴏsᴇ ✖️', callback_data='close')]
                    ])
                )
            except Exception as e:
                print(f"! Error Occured on callback data = 'autodel_cmd' : {e}")
            
    elif data == 'chng_autodel':
        if await authoUser(query, query.from_user.id, owner_only=True):              
            try:
                timer = convert_time(await get_del_timer())
                pic, autodel_mode, mode = await fileSettings(get_auto_delete, set_auto_delete, delfunc=True)
            
                await query.edit_message_media(
                    InputMediaPhoto(pic,
                                    AUTODEL_CMD_TXT.format(
                                        autodel_mode = autodel_mode,
                                        timer = timer
                                    )
                    ),
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton(mode, callback_data='chng_autodel'), InlineKeyboardButton('◈ Sᴇᴛ Tɪᴍᴇʀ ⏱', callback_data='set_timer')],
                        [InlineKeyboardButton('🔄 Rᴇғʀᴇsʜ', callback_data='autodel_cmd'), InlineKeyboardButton('Cʟᴏsᴇ ✖️', callback_data='close')]
                    ])
                )
            except Exception as e:
                print(f"! Error Occured on callback data = 'chng_autodel' : {e}")

    elif data == 'set_timer':
        id = query.from_user.id
        if await authoUser(query, id, owner_only=True):  
            try:
                timer = convert_time(await get_del_timer())
                set_msg = await client.ask(chat_id = id, text=f'<b><blockquote>⏱ Cᴜʀʀᴇɴᴛ Tɪᴍᴇʀ: {timer}</blockquote>\n\nTᴏ ᴄʜᴀɴɢᴇ ᴛɪᴍᴇʀ, Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ɪɴ sᴇᴄᴏɴᴅs ᴡɪᴛʜɪɴ 1 ᴍɪɴᴜᴛᴇ.\n<blockquote>Fᴏʀ ᴇxᴀᴍᴘʟᴇ: <code>300</code>, <code>600</code>, <code>900</code></b></blockquote>', timeout=60)
                del_timer = set_msg.text.split()
                
                if len(del_timer) == 1 and del_timer[0].isdigit():
                    DEL_TIMER = int(del_timer[0])
                    await set_del_timer(DEL_TIMER)
                    timer = convert_time(DEL_TIMER)
                    await set_msg.reply(f"<b><i>Aᴅᴅᴇᴅ Sᴜᴄcᴇssғᴜʟʟʏ ✅</i>\n<blockquote>⏱ Cᴜʀʀᴇɴᴛ Tɪᴍᴇʀ: {timer}</blockquote></b>")
                else:
                    markup = [[InlineKeyboardButton('◈ Sᴇᴛ Dᴇʟᴇᴛᴇ Tɪᴍᴇʀ ⏱', callback_data='set_timer')]]
                    return await set_msg.reply("<b>Pʟᴇᴀsᴇ sᴇɴᴅ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ɪɴ sᴇᴄᴏɴᴅs.\n<blockquote>Fᴏʀ ᴇxᴀᴍᴘʟᴇ: <code>300</code>, <code>600</code>, <code>900</code></blockquote>\n\n<i>Tʀʏ ᴀɢᴀɪɴ ʙʏ ᴄʟɪᴄᴋɪɴɢ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ..</i></b>", reply_markup=InlineKeyboardMarkup(markup))

            except Exception as e:
                try:
                    await set_msg.reply(f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")
                    print(f"! Error Occured on callback data = 'set_timer' : {e}")
                except:
                    await client.send_message(id, text=f"<b>! Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ..\n<blockquote><i>Rᴇᴀsᴏɴ: 1 minute Time out ..</i></b></blockquote>", disable_notification=True)
                    print(f"! Error Occured on callback data = 'set_timer' -> Rᴇᴀsᴏɴ: 1 minute Time out ..")
                    
                
                    
                 
