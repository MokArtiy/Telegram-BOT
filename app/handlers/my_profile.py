import asyncio

from aiogram import F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from ..database.requests import check_ban_user
from ..keyboards import gpt_kb
from ..states.states import WorkGPT, InfAboutFriend

async def plug(callback: CallbackQuery):
    await callback.answer(text='Разраб школьник, нихуя не успел 👎\n'
                               'Появится в следующих обновлениях, следите за новостями!',
                          show_alert=True)