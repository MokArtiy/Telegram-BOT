from aiogram import F, html
from aiogram.types import Message

from ..keyboards import main_kb


async def get_start(message: Message):
    await message.answer(
        text=f"Добро пожаловать в {html.link('NewYear-Bot', 'https://t.me/new_artem_year_bot')}\n"
             f"Выберете, что вы хотите сделать в меню ниже ⬇️",
        reply_markup=main_kb.main_menu, parse_mode="html"
    )