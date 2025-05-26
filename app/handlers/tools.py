import asyncio
import uuid

from aiogram import F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from ..database import requests as rq
from ..database.requests import check_ban_user
from ..keyboards import tools_kb
from ..states.states import WorkGPT, InfAboutFriend
from ..utils import get_media as gm

async def return_to_tools(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.clear()
    await callback.answer('')
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Воспользуйтесь возможностями бота для решения любых задач!', 
        ), 
        reply_markup=tools_kb.tools_main_kb
    )

async def tools_main_menu(callback: CallbackQuery):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
        
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Воспользуйтесь возможностями бота для решения любых задач!', 
        ), 
        reply_markup=tools_kb.tools_main_kb
    )
    
#TO-DO
async def return_to_todo(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.clear()    
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Это меню вашего персонального менеджера задач.\nВыберете действие ниже ⬇️', 
        ), 
        reply_markup=tools_kb.todo_main_kb
    ) 

async def todo_main(callback: CallbackQuery):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Это меню вашего персонального менеджера задач.\nВыберете действие ниже ⬇️', 
        ), 
        reply_markup=tools_kb.todo_main_kb
    )
    
async def add_task(callback: CallbackQuery):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
        
    await callback.answer('')
    
    task_id = str(uuid.uuid4())
    user_id = callback.from_user.id
    task = await rq.get_unsave_task(task_id=task_id, user_id=user_id)
    name = task.name if task.name is not None else '🚫'
    description = task.description if task.description is not None else '🚫'
    deadline = '✔️' if task.deadline is not None else '🚫'
    status = 'сохранено' if task.task_check is True else 'не сохранено'
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption=f'Это меню добавления новых задач в ваш список дел.\nВыберете действие ниже ⬇️\n\n'
                    f'*Название:* {name}\n'
                    f'*Описание:* {description}\n'
                    f'*Дедлайн*: {deadline}\n'
                    f'*Статус*: {status}\n',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.todo_add_task_kb
    )