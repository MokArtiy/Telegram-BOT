from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

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

#ДЕНЬ РОЖДЕНИЯ 31.10.2025
read_from_key = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Прочитать сообщения! 📨', callback_data='read_messages')
        ]
    ]
)

four_msg = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='У вас ещё 5 непрочитанных сообщения! 📨', callback_data='four_msg')
        ]
    ]
)

free_msg = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='У вас ещё 4 непрочитанных сообщения! 📨', callback_data='free_msg')
        ]
    ]
)

two_msg = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='У вас ещё 3 непрочитанных сообщения! 📨', callback_data='two_msg')
        ]
    ]
)

one_msg = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='У вас ещё 2 непрочитанное сообщение! 📨', callback_data='one_msg')
        ]
    ]
)

final_code_msg = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='У вас ещё 1 непрочитанное сообщение! 📨', callback_data='final_code_msg')
        ]
    ]
)

final_msg = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Ввести код! ✍', callback_data='final_msg')
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

celebrate_lemur = ReplyKeyboardMarkup(
    keyboard=
    [
        [
            KeyboardButton(text='Поймать лемура! 🦊', web_app=WebAppInfo(url="https://mokartiy.github.io/Telegram-BOT/"))
        ]
    ],
    resize_keyboard=True
)
celebrate_lemur_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Поймать лемура! 🦊', web_app=WebAppInfo(url="https://mokartiy.github.io/Telegram-BOT/"))
        ]
    ]
)

# #НОВЫЙ ГОД 31.12.25
def generate_results_kb(key: str, value: str) -> InlineKeyboardMarkup: 
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=value, callback_data=key
            )
        ]
    )
    
    return keyboard

def get_photo_keyboard(current_index: int, total: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if current_index == 0:
        builder.button(text="Подвести итоги 🎄", callback_data="start_results")
    
    elif current_index == total - 1:
        builder.button(text="❮", callback_data=f"card_{current_index - 1}")
        builder.button(text="Это было круто 🎉", callback_data="was_cool")
        builder.adjust(2)
    
    else:
        # Промежуточные страницы: "<" и ">"
        builder.button(text="❮", callback_data=f"card_{current_index - 1}")
        builder.button(text="❯", callback_data=f"card_{current_index + 1}")
        builder.adjust(2)
    
    return builder.as_markup()