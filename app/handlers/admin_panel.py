import os
from dotenv import load_dotenv
import asyncio

from aiogram import F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from ..database import requests as rq
from ..keyboards import admin_kb
from ..states.states import AdminPanel


load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')


async def return_to_panel(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.edit_media(
        InputMediaPhoto(
            caption='Вы вошли в панель администратора!\nВыберете действие ниже ⬇️',
            media=FSInputFile(path="image/main-kb.png")
        ),
        reply_markup=admin_kb.main_admin_kb
    )
    
async def return_to_list(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.delete()
    await state.clear()
    await callback.message.answer_photo(
        photo=FSInputFile(path="image/main-kb.png"),
        caption='Вот список всех пользователей бота.\nЧтобы ознакомиться с информацией о пользователе '
             'подробнее, выберете его в списке ниже ⬇️',
        reply_markup=await admin_kb.users_list()
    )

async def return_to_ban_list(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.delete()
    await state.clear()
    await callback.message.answer_photo(
        photo=FSInputFile(path="image/main-kb.png"),
        caption='Вот список забаненных пользователей бота.\nЧтобы ознакомиться с информацией о пользователе '
             'подробнее, выберете его в списке ниже ⬇️',
        reply_markup=await admin_kb.users_bans_list()
    )

async def admin_main_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            caption='Вы вошли в панель администратора!\nВыберете действие ниже ⬇️',
            media=FSInputFile(path="image/main-kb.png")
        ),
        reply_markup=admin_kb.main_admin_kb
    )
    
async def admin_users_list(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            caption='Вот список всех пользователей бота.\nЧтобы ознакомиться с информацией о пользователе '
                    'подробнее, выберете его в списке ниже ⬇️',
            media=FSInputFile(path="image/main-kb.png")
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
            media=FSInputFile(path="image/main-kb.png"),
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
    