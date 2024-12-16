from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

gpt_main_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
            text='Расскажи анекдот', callback_data='anecdote'
            ),
            InlineKeyboardButton(
                text='Что подарить другу?', callback_data='present_4_friend'
            )
        ],
        [
            InlineKeyboardButton(
                text='Задать свой вопрос', callback_data='custom_question'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

next_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Закончить диалог', callback_data='stop_dialog'),
            InlineKeyboardButton(text='На главную', callback_data='to_main')
        ]
    ]
)