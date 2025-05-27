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
                text='Выполненные', callback_data='archived_tasks'
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

todo_add_task_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            
            InlineKeyboardButton(
                text='Название', callback_data='task_name'
            ),
            InlineKeyboardButton(
                text='Описание', callback_data='task_description'
            ),
            InlineKeyboardButton(
                text='Дедлайн', callback_data='task_deadline'
            )
        ],
        [
            InlineKeyboardButton(
                text='Сохранить', callback_data='task_save'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_todo'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

return_from_edit_task_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_create_task'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)