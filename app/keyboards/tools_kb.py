from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

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

todo_description_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Показать сообщение', callback_data='show_description_msg'
            )
        ],
        [
            InlineKeyboardButton(
                text='Текст описания', callback_data='description_caption'
            ),
            InlineKeyboardButton(
                text='Медиа описания', callback_data='description_media'
            )
        ],
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

delete_description_text = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Удалить текст', callback_data='delete_description_text'
            ),
            InlineKeyboardButton(
                text='Изменить медиа', callback_data='description_media'
            )
        ]
    ]
)

delete_description_media = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_create_description'
            ),
            InlineKeyboardButton(
                text='Удалить медиа', callback_data='delete_description_media'
            )
        ]
    ]
)

return_from_edit_description = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_create_description'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

return_from_input_name = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Стандартное значение', callback_data='none_value'
            )
        ],
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

return_from_input_description = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Стандартное значение', callback_data='none_value'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_create_description'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

return_from_show_msg = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_from_show_msg'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

task_deadline_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Инструкция 📖', web_app=WebAppInfo(url='https://mokartiy.github.io/Telegram-BOT/')
            )
        ],
        [
            InlineKeyboardButton(
                text='Дата и время', callback_data='date_and_time'
            ),
            InlineKeyboardButton(
                text='Повтор', callback_data='task_repeat'
            )
        ],
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