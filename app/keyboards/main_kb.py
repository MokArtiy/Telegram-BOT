from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = InlineKeyboardMarkup(inline_keyboard=[
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
            text='Поговорить с GPT', callback_data='gpt_chat'
        )
    ]
])