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
            InlineKeyboardButton(text='Задать ещё вопрос', callback_data='more_question'),
        ],
        [
            InlineKeyboardButton(text='Закончить диалог', callback_data='stop_dialog_in_ai'),
            InlineKeyboardButton(text='На главную', callback_data='to_main_from_ai')
        ]
    ]
)

next_anecdote_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Сгенерировать ещё анекдот', callback_data='more_anecdote')
        ],
        [
            InlineKeyboardButton(text='Закончить диалог', callback_data='stop_dialog'),
            InlineKeyboardButton(text='На главную', callback_data='to_main')
        ]
    ]
)

next_presents_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Сгенерировать ещё варианты', callback_data='more_presents')
        ],
        [
            InlineKeyboardButton(text='Закончить диалог', callback_data='stop_dialog'),
            InlineKeyboardButton(text='На главную', callback_data='to_main')
        ]
    ]
)

gender_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Мужской', callback_data='men_fr'),
            InlineKeyboardButton(text='Женский', callback_data='women_fr'),
        ]
    ]
)