import os
from dotenv import load_dotenv

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
ADMIN_ID = os.getenv('ADMIN_ID')

def main_menu_1 (user_tg_id: int):
    inline_kb=[
        [
            InlineKeyboardButton(
                text='Ввести ключ', callback_data='secret_key'
            )
        ],
        [
            InlineKeyboardButton(
                text='Мой профиль', callback_data='my_profile'
            ),
            InlineKeyboardButton(
                text='Поддержка', callback_data='support_team'
            )
        ],
        [
            InlineKeyboardButton(
                text='Инструменты', callback_data='utils'
            ),
            InlineKeyboardButton(
                text='Поговорить с GPT', callback_data='gpt'
            )
        ]
    ]
    if user_tg_id == int(ADMIN_ID):
        inline_kb.append(
            [
                InlineKeyboardButton(
                    text='Админ панель', callback_data='admin_panel'
                )
            ]
        )
    main_menu_kb = InlineKeyboardMarkup(inline_keyboard=inline_kb)
    return main_menu_kb