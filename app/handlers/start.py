from aiogram import F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from ..database.requests import check_ban_user
from ..keyboards import main_kb
from ..database import requests as rq
from ..utils import get_media as gm

async def get_start(message: Message, state: FSMContext):
    await state.clear()
    await rq.set_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    
    if (await check_ban_user(message.from_user.id)):
        return await message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await message.answer_photo(
        photo=gm.Media_tg.main_photo,
        caption=f"Добро пожаловать в {html.link('NewYear-Bot', 'https://t.me/new_artem_year_bot')}!\n"
             f"Выберете, что вы хотите сделать в меню ниже ⬇️",
        reply_markup=main_kb.main_menu_1(message.from_user.id)
    )

async def to_main(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    await state.clear()
    
    sending = await rq.get_edit_current_sending()
    if sending: 
        await rq.update_edit_status(sending_id=sending.sending_id, status=False)
    
    if (await check_ban_user(callback.from_user.id)):
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.main_photo,
            caption=f"Добро пожаловать в {html.link('NewYear-Bot', 'https://t.me/new_artem_year_bot')}!\n"
            f"Выберете, что вы хотите сделать в меню ниже ⬇️",
        ), reply_markup=main_kb.main_menu_1(callback.from_user.id)
    )

async def photo_inf(message: Message):
    photo_data = message.photo[-1]
    await message.answer(f'{photo_data.file_id}')