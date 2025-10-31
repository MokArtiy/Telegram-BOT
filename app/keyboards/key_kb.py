from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

key_main_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Ввести ключ', callback_data='input_key'),
            InlineKeyboardButton(text='На главную', callback_data='to_main')
        ]
    ]
)

return_key_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Назад', callback_data='return_to_key'),
            InlineKeyboardButton(text='На главную', callback_data='to_main')
        ]
    ]
)

get_gift = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Забрать подарок! 🎁', callback_data='get_gift')
        ]
    ]
)

return_from_gift_key_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Назад', callback_data='return_to_key_from_gift'),
            InlineKeyboardButton(text='На главную', callback_data='to_main_from_gift')
        ]
    ]
)

#ВРЕМЕННО УДАЛИТЬ
celebrate_lemur_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Поймать лемура! 🦊', web_app=WebAppInfo(url="https://mokartiy.github.io/Telegram-BOT/"))
        ]
    ]
)