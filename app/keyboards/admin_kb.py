from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..database.requests import get_users, get_banned_users

main_admin_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Список пользователей', callback_data='users_list'
            ),
            InlineKeyboardButton(
                text='Рассылка сообщений', callback_data='sending_msg'
            )
        ],
        [
            InlineKeyboardButton(
                text='Бан лист', callback_data='ban_users'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

user_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Забанить', callback_data='ban_user'
            ),
            InlineKeyboardButton(
                text='Разбанить', callback_data='unban_user'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_list'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

banned_user_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Забанить', callback_data='ban_user_in_ban'
            ),
            InlineKeyboardButton(
                text='Разбанить', callback_data='unban_user_in_ban'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_ban_list'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

async def users_list():
    all_users = await get_users()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='return_to_panel'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    for user in all_users:
        keyboard.add(
            InlineKeyboardButton(text=f'{str(user.id)}. {user.first_name}', callback_data=f"user_{user.tg_id}")
        )
    return keyboard.adjust(2, 3).as_markup()

async def users_bans_list():
    all_bans = await get_banned_users()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='return_to_panel'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    for user in all_bans:
        keyboard.add(
            InlineKeyboardButton(text=f'{str(user.id)}. {user.first_name}', callback_data=f"bans_{user.tg_id}")
        )
    return keyboard.adjust(2, 3).as_markup()