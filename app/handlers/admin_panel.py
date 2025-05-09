import os
from dotenv import load_dotenv
import asyncio
import logging
import uuid

from aiogram import F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from ..database import requests as rq
from ..keyboards import admin_kb
from ..states.states import AdminPanel
from ..utils import get_media as gm


load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')


async def return_to_panel(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.edit_media(
        InputMediaPhoto(
            caption='Вы вошли в панель администратора!\nВыберете действие ниже ⬇️',
            media=gm.Media_tg.admin_photo
        ),
        reply_markup=admin_kb.main_admin_kb
    )
    
async def return_to_list(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.delete()
    await state.clear()
    await callback.message.answer_photo(
        photo=gm.Media_tg.admin_photo,
        caption='Вот список всех пользователей бота.\nЧтобы ознакомиться с информацией о пользователе '
             'подробнее, выберете его в списке ниже ⬇️',
        reply_markup=await admin_kb.users_list()
    )

async def return_to_ban_list(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.delete()
    await state.clear()
    await callback.message.answer_photo(
        photo=gm.Media_tg.admin_photo,
        caption='Вот список забаненных пользователей бота.\nЧтобы ознакомиться с информацией о пользователе '
             'подробнее, выберете его в списке ниже ⬇️',
        reply_markup=await admin_kb.users_bans_list()
    )

async def return_to_sending_msg(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Это меню рассылок сообщений.\nВыберете действие ниже ⬇️'
        ),
        reply_markup=admin_kb.main_sending_msg_kb
    )

async def admin_main_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            caption='Вы вошли в панель администратора!\nВыберете действие ниже ⬇️',
            media=gm.Media_tg.admin_photo
        ),
        reply_markup=admin_kb.main_admin_kb
    )
    
async def admin_users_list(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            caption='Вот список всех пользователей бота.\nЧтобы ознакомиться с информацией о пользователе '
                    'подробнее, выберете его в списке ниже ⬇️',
            media=gm.Media_tg.admin_photo
        ),
        reply_markup=await admin_kb.users_list()
    )
    
async def get_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(AdminPanel.check_user)
    user_data = await rq.get_userlist_user(callback.data.split('_')[1])
    await state.update_data(check_user=user_data.tg_id)
    if user_data.banned:
        a = '✅'
    else:
        a = 'Not Banned'
    await callback.message.delete()
    msg = await callback.message.answer(
        text=f'Вы просматриваете информацию о пользователе [{user_data.first_name}](tg://user?id={user_data.tg_id})\n'
             f'👉🏻 [ссылка для просмотра](tg://openmessage?user_id={user_data.tg_id}) 👈🏻\n\n'
             f'Telegram ID: `{user_data.tg_id}`\n'
             f'First Name: `{user_data.first_name}`\n'
             f'UserName: `{user_data.username}`\n'
             f'Description: `{user_data.description}`\n'
             f'Phone Number: `{user_data.phone_number}`\n'
             f'Banned: {a}\n',
        reply_markup=admin_kb.user_kb,
        parse_mode='markdown'
    )
    
async def bun_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    data = await state.get_data()
    user_tg_id = data["check_user"]
    user_data = await rq.get_userlist_user(user_tg_id=user_tg_id)
    
    if user_tg_id == int(ADMIN_ID):
        msg = await callback.message.answer(text='Вы не можете применить команду на себя!')
        await asyncio.sleep(5)
        return await msg.delete()
    if user_data.banned == True:
        msg = await callback.message.answer(text='Данный пользователь уже забанен!')
        await asyncio.sleep(5)
        return await msg.delete()
    
    update_data = {
        'Description' : None,
        'Phone Number' : None,
        'Banned' : True
    }
    await rq.update_user(user_tg_id=user_tg_id, data=update_data)
        
    await callback.message.edit_text(
        text=f'Вы просматриваете информацию о пользователе [{user_data.first_name}](tg://user?id={user_data.tg_id})\n'
             f'👉🏻 [ссылка для просмотра](tg://openmessage?user_id={user_data.tg_id}) 👈🏻\n\n'
             f'Telegram ID: `{user_data.tg_id}`\n'
             f'First Name: `{user_data.first_name}`\n'
             f'UserName: `{user_data.username}`\n'
             f'Description: `{user_data.description}`\n'
             f'Phone Number: `{user_data.phone_number}`\n'
             f'Banned: ✅',
        reply_markup=admin_kb.user_kb,
        parse_mode='markdown'
    )
    
async def unban_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    data = await state.get_data()
    user_tg_id = data["check_user"]
    user_data = await rq.get_userlist_user(user_tg_id=user_tg_id)
    
    if user_tg_id == int(ADMIN_ID):
        msg = await callback.message.answer(text='Вы не можете применить команду на себя!')
        await asyncio.sleep(5)
        return await msg.delete()
    if user_data.banned == False:
        msg = await callback.message.answer(text='Данный пользователь уже разбанен!')
        await asyncio.sleep(5)
        return await msg.delete()
        
    update_data = {
        'Description' : None,
        'Phone Number' : None,
        'Banned' : False
    }
    await rq.update_user(user_tg_id=user_tg_id, data=update_data)
    await callback.message.edit_text(
        text=f'Вы просматриваете информацию о пользователе [{user_data.first_name}](tg://user?id={user_data.tg_id})\n'
             f'👉🏻 [ссылка для просмотра](tg://openmessage?user_id={user_data.tg_id}) 👈🏻\n\n'
             f'Telegram ID: `{user_data.tg_id}`\n'
             f'First Name: `{user_data.first_name}`\n'
             f'UserName: `{user_data.username}`\n'
             f'Description: `{user_data.description}`\n'
             f'Phone Number: `{user_data.phone_number}`\n'
             f'Banned: Not Banned',
        reply_markup=admin_kb.user_kb,
        parse_mode='markdown'
    )
    
async def get_list_banned_users(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Вот список забаненных пользователей бота.\nЧтобы ознакомиться с информацией о пользователе '
                    'подробнее, выберете его в списке ниже ⬇️'
        ),
        reply_markup=await admin_kb.users_bans_list()
    )

async def get_banned_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(AdminPanel.check_user)
    user_data = await rq.get_userlist_user(callback.data.split('_')[1])
    await state.update_data(check_user=user_data.tg_id)
    if user_data.banned:
        a = '✅'
    else:
        a = 'Not Banned'
    await callback.message.delete()
    msg = await callback.message.answer(
        text=f'Вы просматриваете информацию о пользователе [{user_data.first_name}](tg://user?id={user_data.tg_id})\n'
             f'👉🏻 [ссылка для просмотра](tg://openmessage?user_id={user_data.tg_id}) 👈🏻\n\n'
             f'Telegram ID: `{user_data.tg_id}`\n'
             f'First Name: `{user_data.first_name}`\n'
             f'UserName: `{user_data.username}`\n'
             f'Description: `{user_data.description}`\n'
             f'Phone Number: `{user_data.phone_number}`\n'
             f'Banned: {a}\n',
        reply_markup=admin_kb.banned_user_kb,
        parse_mode='markdown'
    )
    
async def unban_user_in_ban(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    data = await state.get_data()
    user_tg_id = data["check_user"]
    user_data = await rq.get_userlist_user(user_tg_id=user_tg_id)
    
    if user_data.banned == False:
        msg = await callback.message.answer(text='Данный пользователь уже разбанен!')
        await asyncio.sleep(5)
        return await msg.delete()
        
    update_data = {
        'Description' : None,
        'Phone Number' : None,
        'Banned' : False
    }
    await rq.update_user(user_tg_id=user_tg_id, data=update_data)
    await callback.message.edit_text(
        text=f'Вы просматриваете информацию о пользователе [{user_data.first_name}](tg://user?id={user_data.tg_id})\n'
             f'👉🏻 [ссылка для просмотра](tg://openmessage?user_id={user_data.tg_id}) 👈🏻\n\n'
             f'Telegram ID: `{user_data.tg_id}`\n'
             f'First Name: `{user_data.first_name}`\n'
             f'UserName: `{user_data.username}`\n'
             f'Description: `{user_data.description}`\n'
             f'Phone Number: `{user_data.phone_number}`\n'
             f'Banned: Not Banned',
        reply_markup=admin_kb.banned_user_kb,
        parse_mode='markdown'
    )
    
async def bun_user_in_ban(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')

    data = await state.get_data()
    user_tg_id = data["check_user"]
    user_data = await rq.get_userlist_user(user_tg_id=user_tg_id)
    
    if user_data.banned == True:
        msg = await callback.message.answer(text='Данный пользователь уже забанен!')
        await asyncio.sleep(5)
        return await msg.delete()
    
    update_data = {
        'Description' : None,
        'Phone Number' : None,
        'Banned' : True
    }
    await rq.update_user(user_tg_id=user_tg_id, data=update_data)
        
    await callback.message.edit_text(
        text=f'Вы просматриваете информацию о пользователе [{user_data.first_name}](tg://user?id={user_data.tg_id})\n'
             f'👉🏻 [ссылка для просмотра](tg://openmessage?user_id={user_data.tg_id}) 👈🏻\n\n'
             f'Telegram ID: `{user_data.tg_id}`\n'
             f'First Name: `{user_data.first_name}`\n'
             f'UserName: `{user_data.username}`\n'
             f'Description: `{user_data.description}`\n'
             f'Phone Number: `{user_data.phone_number}`\n'
             f'Banned: ✅',
        reply_markup=admin_kb.banned_user_kb,
        parse_mode='markdown'
    )

#SENDING MESSAGE
async def return_to_create_msg(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    
    sending = await rq.get_unsave_sending()
    recipients_mark = await rq.get_recipients_sending(sending_id=sending.sending_id)
    
    name = sending.sending_name if sending.sending_name is not None else '🚫'
    text = sending.message_text if sending.message_text is not None else '🚫'
    if len(text) > 450:
        text = '✔️'
        
    media = '✔️' if sending.message_media is not None else '🚫'
    recipient = '✔️' if recipients_mark.all() else '🚫'
    time = sending.sending_time if sending.sending_time is not None else '🚫'
    status = 'сохранено' if sending.sending_check is True else 'не сохранено'
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption=f'Создать новый сценарий рассылки:\n\n'
                    f'*Название:* {name}\n'
                    f'*Текст:* {text}\n'
                    f'*Медиа:* {media}\n'
                    f'*Люди:* {recipient}\n'
                    f'*Время:* {time}\n'
                    f'*Статус:* {status}\n',
            parse_mode='markdown'
        ),
        reply_markup=admin_kb.create_sending_kb
    )

async def sending_msg(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Это меню рассылок сообщений.\nВыберете действие ниже ⬇️'
        ),
        reply_markup=admin_kb.main_sending_msg_kb
    )

async def create_sending(callback: CallbackQuery):
    await callback.answer('')
    
    sending_id = str(uuid.uuid4())
    sending = await rq.get_unsave_sending(sending_id=sending_id)
    recipients_mark = await rq.get_recipients_sending(sending_id=sending.sending_id)
    
    name = sending.sending_name if sending.sending_name is not None else '🚫'
    text = sending.message_text if sending.message_text is not None else '🚫'
    if len(text) > 450:
        text = '✔️'
    
    media = '✔️' if sending.message_media is not None else '🚫'
    recipient = '✔️' if recipients_mark.all() else '🚫'
    time = sending.sending_time if sending.sending_time is not None else '🚫'
    status = 'сохранено' if sending.sending_check is True else 'не сохранено'
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption=f'Создать новый сценарий рассылки:\n\n'
                    f'*Название:* {name}\n'
                    f'*Текст:* {text}\n'
                    f'*Медиа:* {media}\n'
                    f'*Люди:* {recipient}\n'
                    f'*Время:* {time}\n'
                    f'*Статус:* {status}\n',
            parse_mode='markdown'
        ),
        reply_markup=admin_kb.create_sending_kb
    )

#edit-name
async def edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(AdminPanel.message_admin_id)
    msg = await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Хорошо, отправь мне новое название для твоей рассылки, только не забывай об ограничении в *32* символа!',
                parse_mode='markdown'
            )
        )
    await state.update_data(message_admin_id=msg.message_id)
    await state.set_state(AdminPanel.edit_name)
    
async def input_name(message: Message, state: FSMContext):
    sending_id = (await rq.get_unsave_sending()).sending_id
    if len(message.text) <= 32:
        data = await state.get_data()
        await rq.update_name(sending_id=sending_id, sending_name=message.text)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Имя рассылки успешно обновлено!'
            ),
            reply_markup=admin_kb.return_from_edit_kb
        )
        await state.clear()
    else:
        data = await state.get_data()
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Имя рассылки не должно превышать *32* символа! Попробуйте снова...',
                parse_mode='markdown'
            ),
            reply_markup=admin_kb.return_from_edit_kb
        )
    
    await message.delete()

#edit-text
async def edit_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    sending = await rq.get_unsave_sending()
    if sending.message_media is not None and (sending.message_media.split())[1] == 'video_note':
        await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Вы уже прикрепили кружок к сообщению! Хотите его удалить?',
                parse_mode='markdown'
            ), 
            reply_markup=admin_kb.delete_media
    )
    elif sending.message_media is not None and (sending.message_media.split())[1] == 'voice':
        return await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Вы уже прикрепили гс к сообщению! Хотите его удалить?',
                parse_mode='markdown'
            ), 
            reply_markup=admin_kb.delete_media
    )
    else:
        await state.set_state(AdminPanel.message_admin_id)
        msg = await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Хорошо, отправь мне текст твоей новой рассылки, только не забывай об ограничении в *1024* символа!',
                parse_mode='markdown'
            )
        )
        await state.update_data(message_admin_id=msg.message_id)
        await state.set_state(AdminPanel.edit_text)
    
async def input_text(message: Message, state: FSMContext):
    sending_id = (await rq.get_unsave_sending()).sending_id
    if len(message.text) <= 1024:
        data = await state.get_data()
        await rq.update_text(sending_id=sending_id, message_text=message.text)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Текст рассылки был обновлён!'
            ),
            reply_markup=admin_kb.return_from_edit_kb
        )
        await state.clear()
    else:
        data = await state.get_data()
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Текст сообщения не должен превышать *1024* символа! Попробуйте снова...',
                parse_mode='markdown'
            ),
            reply_markup=admin_kb.return_from_edit_kb
        )
    
    await message.delete()

#edit-media    
async def edit_media(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(AdminPanel.message_admin_id)
    msg = await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Хорошо, отправьте мне фото, видео, кружок, голосовое сообщение, аудио или документ',
            parse_mode='markdown'
        )
    )
    await state.update_data(message_admin_id=msg.message_id)
    await state.set_state(AdminPanel.edit_media)

async def input_media(message: Message, state: FSMContext):
    sending = await rq.get_unsave_sending()
    if message.content_type == 'photo':
        data = await state.get_data()
        message_media = (message.photo[-1]).file_id + ' photo'
        await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Медиа рассылки было успешно обновлено!'
            ), 
            reply_markup=admin_kb.return_from_edit_kb
        )
        await state.clear()
    elif message.content_type == 'video':
        data = await state.get_data()
        message_media = message.video.file_id + ' video'
        await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Медиа рассылки было успешно обновлено!'
            ), 
            reply_markup=admin_kb.return_from_edit_kb
        )
        await state.clear()
    elif message.content_type == 'video_note':
        await state.update_data(edit_media=message.video_note.file_id + ' video_note')
        data = await state.get_data()
        if sending.message_text is not None:
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_admin_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='Вы пытаетесь создать сообщение с видео-кружком. У такого вида сообщений нету параметра *текст*!'
                            'Удалите параметр *текст* или измените медиа файл!',
                    parse_mode='markdown'
                ), 
                reply_markup=admin_kb.delete_text
            )
        else:
            message_media = message.video_note.file_id + ' video_note'
            await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_admin_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='Успех! Медиа рассылки было успешно обновлено!'
                ), 
                reply_markup=admin_kb.return_from_edit_kb
            )
            await state.clear()
    elif message.content_type == 'audio':
        data = await state.get_data()
        message_media = message.audio.file_id + ' audio'
        await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Медиа рассылки было успешно обновлено!'
            ), 
            reply_markup=admin_kb.return_from_edit_kb
        )
        await state.clear()
    elif message.content_type == 'voice':
        await state.update_data(edit_media=message.voice.file_id + ' voice')
        data = await state.get_data()
        if sending.message_text is not None:
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_admin_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='Вы пытаетесь создать сообщение с гс. У такого вида сообщений нету параметра *текст*!'
                            'Удалите параметр *текст* или измените медиа файл!',
                    parse_mode='markdown'
                ), 
                reply_markup=admin_kb.delete_text
            )
        else:
            message_media = message.voice.file_id + ' voice'
            await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_admin_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='Успех! Медиа рассылки было успешно обновлено!'
                ), 
                reply_markup=admin_kb.return_from_edit_kb
            )
            await state.clear()
    elif message.content_type == 'document':
        data = await state.get_data()
        message_media = message.document.file_id + ' document'
        await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Медиа рассылки было успешно обновлено!'
            ), 
            reply_markup=admin_kb.return_from_edit_kb
        )
        await state.clear()
    elif message.content_type == 'text' and message.text == 'None':
        data = await state.get_data()
        message_media = None
        await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Медиа рассылки было успешно обновлено!'
            ), 
            reply_markup=admin_kb.return_from_edit_kb
        )
        await state.clear()
    else:
        data = await state.get_data()
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Отправленное вами сообщение не подходит под обрабатываемые типы медиа! Попробуйте снова...',
                parse_mode='markdown'
            ),
            reply_markup=admin_kb.return_from_edit_kb
        )
        
    await message.delete()
    
async def delete_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    sending_id = (await rq.get_unsave_sending()).sending_id
    data = await state.get_data()
    await rq.update_media(sending_id=sending_id, message_media=data['edit_media'])
    await rq.delete_text()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Текст успешно удалён!'
        ),
        reply_markup=admin_kb.return_from_edit_kb
    )
    await state.clear()
    
async def delete_media(callback: CallbackQuery):
    await callback.answer('')
    await rq.delete_media()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Медиа успешно удалено!'
        ),
        reply_markup=admin_kb.return_from_edit_kb
    )

#edit-recipients
async def return_to_recipients(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Выберете готовый пресет или настройте рассылку самостоятельно ⬇️'
        ),
        reply_markup=admin_kb.edit_recipients_kb
    )

async def edit_recipients(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Выберете готовый пресет или настройте рассылку самостоятельно ⬇️'
        ),
        reply_markup=admin_kb.edit_recipients_kb
    )

async def choose_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Выберете один из готовых пресетов ниже ⬇️'
        ),
        reply_markup=await admin_kb.ready_presets_list()
    )
    
async def choose_save_preset(callback: CallbackQuery):
    sending_id = (await rq.get_unsave_sending()).sending_id
    sending_preset_id = await rq.get_sending_preset_id(sending_id=sending_id)
    if sending_preset_id is not None and sending_preset_id == callback.data.split('_')[1]:
        await callback.answer('Этот пресет уже выбран!', show_alert=True)
    else:
        if callback.data.split('_')[1] == 'ALL':
            sending_id = (await rq.get_unsave_sending()).sending_id
            await rq.add_recipient_all_preset(sending_id=sending_id)
        
        await rq.update_sending_preset(sending_id=sending_id, preset_id=callback.data.split('_')[1])
        await callback.answer('Пресет успешно применён!', show_alert=True)

async def delete_current_preset(callback: CallbackQuery):
    sending_id = (await rq.get_unsave_sending()).sending_id
    sending_preset_id = await rq.get_sending_preset_id(sending_id=sending_id)
    if sending_preset_id is not None:
        await rq.remove_current_preset(sending_id=sending_id, preset_id=sending_preset_id)
        await callback.answer('Текущий пресет был успешно удалён!', show_alert=True)
    else:
        await callback.answer('У рассылки нет текущего пресета!', show_alert=True)

#manage-presets
async def return_to_manage_presets(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Вы в меню управления готовыми пресетами.\nВыберете действие ниже ⬇️'
        ),
        reply_markup=await admin_kb.presets_list()
    )

async def manage_presets(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Вы в меню управления готовыми пресетами.\nВыберете действие ниже ⬇️'
        ),
        reply_markup=await admin_kb.presets_list()
    )
    
async def create_preset(callback: CallbackQuery):
    await callback.answer('')
    
    preset_id = str(uuid.uuid4())
    preset = await rq.get_unsave_presets(preset_id=preset_id)
    
    preset_name = preset.preset_name if preset.preset_name is not None else '🚫'
    if (await rq.get_recipients_preset(preset_id=preset.preset_id)).all():
        recipients = (await rq.get_recipients_preset(preset_id=preset.preset_id)).all()
    else:
        recipients = '🚫'
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption=f'Создать новый пресет получателей:\n\n'
                    f'*Название:* {preset_name}\n'
                    f'*Люди:* {recipients}\n',
            parse_mode='markdown'
        ),
        reply_markup=admin_kb.create_preset_kb
    )
    
#create-sending-save
async def save_sending(callback: CallbackQuery):
    sending_id = (await rq.get_unsave_sending()).sending_id
    if (await rq.update_status(sending_id=sending_id) == 0):
        await callback.answer('Рассылка должна содержать название, текст/медиа, пресет получателей!', show_alert=True)
    elif (await rq.update_status(sending_id=sending_id) == 1):
        await callback.answer('Рассылка успешно создана!', show_alert=True)
        
        await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Это меню рассылок сообщений.\nВыберете действие ниже ⬇️'
        ),
        reply_markup=admin_kb.main_sending_msg_kb
    )

#manage-sending
async def return_to_manage_sending(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    await state.clear()
    sending = await rq.get_edit_current_sending()
    await rq.update_edit_status(sending_id=sending.sending_id, status=False)
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Вы в меню управления сохранённых рассылок.\nВыберете действие ниже ⬇️'
        ),
        reply_markup=await admin_kb.sendings_list()
    )
    
async def return_to_manage_current_sending(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    sending = await rq.get_edit_current_sending()
    
    name = sending.sending_name
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption=f'Вы в меню управления рассылкой *{name}*.\nВыберете действие ниже ⬇️',
            parse_mode='markdown'
        ),
        reply_markup=admin_kb.manage_sending_kb
    )

async def return_to_edit_current_sending(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    sending = await rq.get_edit_current_sending()
    recipients_mark = await rq.get_recipients_sending(sending_id=sending.sending_id)
    
    name = sending.sending_name if sending.sending_name is not None else '🚫'
    text = sending.message_text if sending.message_text is not None else '🚫'
    if len(text) > 450:
        text = '✔️'
    
    media = '✔️' if sending.message_media is not None else '🚫'
    recipient = '✔️' if recipients_mark.all() else '🚫'
    time = sending.sending_time if sending.sending_time is not None else '🚫'
    status = 'сохранено' if sending.sending_check is True else 'не сохранено'
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption=f'Изменить текущую рассылку:\n\n'
                    f'*Название:* {name}\n'
                    f'*Текст:* {text}\n'
                    f'*Медиа:* {media}\n'
                    f'*Люди:* {recipient}\n'
                    f'*Время:* {time}\n'
                    f'*Статус:* {status}\n',
            parse_mode='markdown'
        ),
        reply_markup=admin_kb.edit_current_sending_kb
    )

async def manage_sending(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Вы в меню управления сохранённых рассылок.\nВыберете действие ниже ⬇️'
        ),
        reply_markup=await admin_kb.sendings_list()
    )
    
async def manage_current_sending(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    sending_id = callback.data.split('_')[1]
    sending = await rq.set_sending(sending_id=sending_id)
    name = sending.sending_name

    await rq.update_edit_status(sending_id=sending_id, status=True)
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption=f'Вы в меню управления рассылкой *{name}*.\nВыберете действие ниже ⬇️',
            parse_mode='markdown'
        ),
        reply_markup=admin_kb.manage_sending_kb
    )

async def run_sending(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    loader_msg = await callback.message.answer('⏳ Идёт обработка...')
    
    sending = await rq.get_edit_current_sending()
    sending_id = sending.sending_id
    
    if(sending.message_text is None and sending.message_media is None) or (sending.sending_name is None or sending.sending_preset_id is None):
        error_msg = await callback.message.answer('❌ Рассылка должна содержать название, текст/медиа и пресет получателей!')
        await asyncio.sleep(5)
        await error_msg.delete()
        await loader_msg.delete()
        return
    type_media = None
    if sending.message_media is not None : type_media = sending.message_media.split(' ')[1]
    
    user_ids = {}
    user_ids.update(await rq.get_all_recipients_ids(sending_id=sending_id, preset_id=sending.sending_preset_id))
    user_ids_list = list(user_ids.keys())
    
    disable_notification: bool = False
    batch_size: int = 30
    delay: float = 1.0
    
    # :param disable_notification: Отключить уведомления
    # :param batch_size: Количество сообщений в одной группе
    # :param delay: Задержка между группами в секундах
    
    success = 0
    failed = 0
    
    for i in range(0, len(user_ids_list), batch_size):
        batch = user_ids_list[i:i + batch_size]
        tasks = []
        
        for user_id in batch:
            try:
                if type_media == 'photo':
                    task = gm.bot.send_photo(
                        chat_id=user_id,
                        photo=sending.message_media.split(' ')[0],
                        caption=sending.message_text,
                        disable_notification=disable_notification
                    )
                elif type_media == 'video':
                    task = gm.bot.send_video(
                        chat_id=user_id,
                        video=sending.message_media.split(' ')[0],
                        caption=sending.message_text,
                        disable_notification=disable_notification
                    )
                elif type_media == 'video_note':
                    task = gm.bot.send_video_note(
                        chat_id=user_id,
                        video_note=sending.message_media.split(' ')[0],
                        disable_notification=disable_notification
                    )
                elif type_media == 'audio':
                    task = gm.bot.send_audio(
                        chat_id=user_id,
                        audio=sending.message_media.split(' ')[0],
                        caption=sending.message_text,
                        disable_notification=disable_notification
                    )
                elif type_media == 'voice':
                    task = gm.bot.send_voice(
                        chat_id=user_id,
                        voice=sending.message_media.split(' ')[0],
                        disable_notification=disable_notification
                    )
                elif type_media == 'document':
                    task = gm.bot.send_document(
                        chat_id=user_id,
                        document=sending.message_media.split(' ')[0],
                        caption=sending.message_text,
                        disable_notification=disable_notification
                    )
                else:
                    task = gm.bot.send_message(
                        chat_id=user_id,
                        text=sending.message_text,
                        disable_notification=disable_notification
                    )
                tasks.append(task)
            except Exception as e:
                logging.error(f"Ошибка при создании задачи для {user_id}: {e}")
                failed += 1
        
        # Выполняем пачку запросов
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, Exception):
                    failed += 1
                    logging.error(f"Ошибка отправки: {res}")
                else:
                    success += 1
        except Exception as e:
            logging.error(f"Ошибка в группе {i//batch_size}: {e}")
            failed += len(batch)
        
        # Задержка между пачками
        if i + batch_size < len(user_ids_list):
            await asyncio.sleep(delay)
    
    await loader_msg.delete()
    status_msg = await callback.message.answer(
        f"📊 Рассылка завершена:\n"
        f"✅ Успешно: {success}\n"
        f"❌ Ошибок: {failed}"
    )
    await asyncio.sleep(5)
    await status_msg.delete()
    
async def edit_current_sending(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    sending = await rq.get_edit_current_sending()
    recipients_mark = await rq.get_recipients_sending(sending_id=sending.sending_id)
    
    name = sending.sending_name if sending.sending_name is not None else '🚫'
    text = sending.message_text if sending.message_text is not None else '🚫'
    if len(text) > 450:
        text = '✔️'
    
    media = '✔️' if sending.message_media is not None else '🚫'
    recipient = '✔️' if recipients_mark.all() else '🚫'
    time = sending.sending_time if sending.sending_time is not None else '🚫'
    status = 'сохранено' if sending.sending_check is True else 'не сохранено'
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption=f'Изменить текущую рассылку:\n\n'
                    f'*Название:* {name}\n'
                    f'*Текст:* {text}\n'
                    f'*Медиа:* {media}\n'
                    f'*Люди:* {recipient}\n'
                    f'*Время:* {time}\n'
                    f'*Статус:* {status}\n',
            parse_mode='markdown'
        ),
        reply_markup=admin_kb.edit_current_sending_kb
    )
    
#edit-current-name
async def edit_current_sending_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(AdminPanel.message_admin_id)
    msg = await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Хорошо, отправь мне новое название для твоей рассылки, только не забывай об ограничении в *32* символа!',
                parse_mode='markdown'
            )
        )
    await state.update_data(message_admin_id=msg.message_id)
    await state.set_state(AdminPanel.edit_current_sending_name)
    
async def input_current_sending_name(message: Message, state: FSMContext):
    data = await state.get_data()
    sending = await rq.get_edit_current_sending()
    sending_id = sending.sending_id
    
    if len(message.text) <= 32:
        data = await state.get_data()
        await rq.update_name(sending_id=sending_id, sending_name=message.text)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Имя рассылки успешно обновлено!'
            ),
            reply_markup=admin_kb.return_from_edit_current_sending_kb
        )
        await state.clear()
    else:
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Имя рассылки не должно превышать *32* символа! Попробуйте снова...',
                parse_mode='markdown'
            ),
            reply_markup=admin_kb.return_from_edit_kb
        )
    
    await message.delete()

# #edit-current-text
async def edit_current_sending_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    sending = await rq.get_edit_current_sending()
    
    if sending.message_media is not None and (sending.message_media.split())[1] == 'video_note':
        await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='К сообщению уже прикреплён кружок! Хотите его удалить?',
                parse_mode='markdown'
            ), 
            reply_markup=admin_kb.delete_current_sending_media
    )
    elif sending.message_media is not None and (sending.message_media.split())[1] == 'voice':
        return await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='К сообщению уже прикреплён гс! Хотите его удалить?',
                parse_mode='markdown'
            ), 
            reply_markup=admin_kb.delete_current_sending_media
    )
    else:
        await state.set_state(AdminPanel.message_admin_id)
        msg = await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Хорошо, отправь мне текст твоей новой рассылки, только не забывай об ограничении в *1024* символа!',
                parse_mode='markdown'
            )
        )
        await state.update_data(message_admin_id=msg.message_id)
        await state.set_state(AdminPanel.edit_current_sending_text)
    
async def input_current_sending_text(message: Message, state: FSMContext):
    data = await state.get_data()
    sending = await rq.get_edit_current_sending()
    sending_id = sending.sending_id
    
    if len(message.text) <= 1024:
        await rq.update_text(sending_id=sending_id, message_text=message.text)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Текст рассылки был обновлён!'
            ),
            reply_markup=admin_kb.return_from_edit_current_sending_kb
        )
        await state.clear()
    else:
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Текст сообщения не должен превышать *1024* символа! Попробуйте снова...',
                parse_mode='markdown'
            ),
            reply_markup=admin_kb.return_from_edit_current_sending_kb
        )
    
    await message.delete()

#edit-current-media    
async def edit_current_sending_media(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(AdminPanel.message_admin_id)
    msg = await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Хорошо, отправьте мне фото, видео, кружок, голосовое сообщение, аудио или документ',
            parse_mode='markdown'
        )
    )
    await state.update_data(message_admin_id=msg.message_id)
    await state.set_state(AdminPanel.edit_current_sending_media)

async def input_current_sending_media(message: Message, state: FSMContext):
    sending = await rq.get_edit_current_sending()
    if message.content_type == 'photo':
        data = await state.get_data()
        message_media = (message.photo[-1]).file_id + ' photo'
        await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Медиа рассылки было успешно обновлено!'
            ), 
            reply_markup=admin_kb.return_from_edit_current_sending_kb
        )
        await state.clear()
    elif message.content_type == 'video':
        data = await state.get_data()
        message_media = message.video.file_id + ' video'
        await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Медиа рассылки было успешно обновлено!'
            ), 
            reply_markup=admin_kb.return_from_edit_current_sending_kb
        )
        await state.clear()
    elif message.content_type == 'video_note':
        await state.update_data(edit_media=message.video_note.file_id + ' video_note')
        data = await state.get_data()
        if sending.message_text is not None:
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_admin_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='Вы пытаетесь создать сообщение с видео-кружком. У такого вида сообщений нету параметра *текст*!'
                            'Удалите параметр *текст* или измените медиа файл!',
                    parse_mode='markdown'
                ), 
                reply_markup=admin_kb.delete_text
            )
        else:
            message_media = message.video_note.file_id + ' video_note'
            await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_admin_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='Успех! Медиа рассылки было успешно обновлено!'
                ), 
                reply_markup=admin_kb.return_from_edit_current_sending_kb
            )
            await state.clear()
    elif message.content_type == 'audio':
        data = await state.get_data()
        message_media = message.audio.file_id + ' audio'
        await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Медиа рассылки было успешно обновлено!'
            ), 
            reply_markup=admin_kb.return_from_edit_current_sending_kb
        )
        await state.clear()
    elif message.content_type == 'voice':
        await state.update_data(edit_media=message.voice.file_id + ' voice')
        data = await state.get_data()
        if sending.message_text is not None:
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_admin_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='Вы пытаетесь создать сообщение с гс. У такого вида сообщений нету параметра *текст*!'
                            'Удалите параметр *текст* или измените медиа файл!',
                    parse_mode='markdown'
                ), 
                reply_markup=admin_kb.delete_text
            )
        else:
            message_media = message.voice.file_id + ' voice'
            await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_admin_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='Успех! Медиа рассылки было успешно обновлено!'
                ), 
                reply_markup=admin_kb.return_from_edit_current_sending_kb
            )
            await state.clear()
    elif message.content_type == 'document':
        data = await state.get_data()
        message_media = message.document.file_id + ' document'
        await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Медиа рассылки было успешно обновлено!'
            ), 
            reply_markup=admin_kb.return_from_edit_current_sending_kb
        )
        await state.clear()
    elif message.content_type == 'text' and message.text == 'None':
        data = await state.get_data()
        message_media = None
        await rq.update_media(sending_id=sending.sending_id, message_media=message_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Успех! Медиа рассылки было успешно обновлено!'
            ), 
            reply_markup=admin_kb.return_from_edit_current_sending_kb
        )
        await state.clear()
    else:
        data = await state.get_data()
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_admin_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.admin_photo,
                caption='Отправленное вами сообщение не подходит под обрабатываемые типы медиа! Попробуйте снова...',
                parse_mode='markdown'
            ),
            reply_markup=admin_kb.return_from_edit_current_sending_kb
        )
        
    await message.delete()

#edit-recipients
async def return_to_current_sending_recipients(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Выберете готовый пресет или настройте рассылку самостоятельно ⬇️'
        ),
        reply_markup=admin_kb.edit_current_sending_recipients_kb
    )

async def edit_current_sending_recipients(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Выберете готовый пресет или настройте рассылку самостоятельно ⬇️'
        ),
        reply_markup=admin_kb.edit_current_sending_recipients_kb
    )

async def choose_current_sending_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Выберете один из готовых пресетов ниже ⬇️'
        ),
        reply_markup=await admin_kb.ready_presets_for_current_sending_list()
    )

async def choose_save_preset_in_current_sending(callback: CallbackQuery):
    sending_id = (await rq.get_edit_current_sending()).sending_id
    sending_preset_id = await rq.get_sending_preset_id(sending_id=sending_id)
    if sending_preset_id is not None and sending_preset_id == callback.data.split('_')[1]:
        await callback.answer('Этот пресет уже выбран!', show_alert=True)
    else:
        if callback.data.split('_')[1] == 'ALL':
            await rq.add_recipient_all_preset(sending_id=sending_id)
        
        await rq.update_sending_preset(sending_id=sending_id, preset_id=callback.data.split('_')[1])
        await callback.answer('Пресет успешно применён!', show_alert=True)

async def delete_current_preset_in_current_sending(callback: CallbackQuery):
    sending_id = (await rq.get_edit_current_sending()).sending_id
    sending_preset_id = await rq.get_sending_preset_id(sending_id=sending_id)
    if sending_preset_id is not None:
        await rq.remove_current_preset(sending_id=sending_id, preset_id=sending_preset_id)
        await callback.answer('Текущий пресет был успешно удалён!', show_alert=True)
    else:
        await callback.answer('У рассылки нет текущего пресета!', show_alert=True)

#delete_current_sending
async def delete_current_sending(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    sending = await rq.get_edit_current_sending()
    
    await state.set_state(AdminPanel.message_admin_id)
    msg = await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption=f'Вы точно хотите удалить рассылку *{sending.sending_name}*?',
            parse_mode='markdown'
        ),
        reply_markup=admin_kb.delete_sending_choose
    )
    await state.update_data(message_admin_id=msg.message_id)

async def yes_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    sending = await rq.get_edit_current_sending()
    await rq.delete_sending(sending.sending_id)
    await callback.answer(f'Рассылка {sending.sending_name} успешно удалена!', show_alert=True)

    await gm.bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=data['message_admin_id'],
        media=InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption='Вы в меню управления сохранённых рассылок.\nВыберете действие ниже ⬇️'
        ),
        reply_markup=await admin_kb.sendings_list()
    )
    
async def no_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sending = await rq.get_edit_current_sending()
    
    await gm.bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=data['message_admin_id'],
        media=InputMediaPhoto(
            media=gm.Media_tg.admin_photo,
            caption=f'Вы в меню управления рассылкой *{sending.sending_name}*.\nВыберете действие ниже ⬇️',
            parse_mode='markdown'
        ),
        reply_markup=admin_kb.manage_sending_kb
    )
    