from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

tools_main_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Список дел (ToDo)', callback_data='todo_main'
            ),
            InlineKeyboardButton(
                text='Кружок из видео', callback_data='video_note_main'
            )
        ],
        [
            InlineKeyboardButton(
                text='Прогноз погоды', callback_data='weather_main'
            ),
            InlineKeyboardButton(
                text='Мировая валюта', callback_data='currency_main'
            )
        ],
        [
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

todo_main_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Добавить задачу', callback_data='add_task'
            )
        ],
        [
            InlineKeyboardButton(
                text='Текущие задачи', callback_data='current_tasks'
            ),
            InlineKeyboardButton(
                text='Выполненные задачи', callback_data='archived_tasks'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_tools'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)