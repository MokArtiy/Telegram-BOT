import asyncio
import uuid
from datetime import datetime

from aiogram import F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from ...database import requests as rq
from ...database.requests import check_ban_user
from ...keyboards import tools_kb
from ...states.states import ToDo
from ...utils import get_media as gm

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
    
