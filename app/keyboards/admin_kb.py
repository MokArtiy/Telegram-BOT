from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..database.requests import get_users, get_banned_users, get_save_presets

main_admin_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Список юзеров', callback_data='users_list'
            ),
            InlineKeyboardButton(
                text='Рассылка', callback_data='sending_msg'
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

main_sending_msg_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Создать', callback_data='create_sending'
            )
        ],
        [
            InlineKeyboardButton(
                text='Управление пресетами', callback_data='manage_presets'
            )  
        ],
        [
            InlineKeyboardButton(
                text='Редактировать', callback_data='edit_sending'
            ),
            InlineKeyboardButton(
                text='Удалить', callback_data='delete_sending'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_panel'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

create_sending_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Изменить текст', callback_data='edit_text'
            ),
            InlineKeyboardButton(
                text='Изменить медиа', callback_data='edit_media'
            )
        ],
        [
            InlineKeyboardButton(
                text='Получатели', callback_data='edit_recipients'
            ),
            InlineKeyboardButton(
                text='Изменить время', callback_data='edit_time'
            )
        ],
        [
            InlineKeyboardButton(
                text='Создать рассылку', callback_data='save_and_create_sending'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_sending_msg'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

return_from_edit_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_create_msg'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

delete_text = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Удалить текст', callback_data='delete_text'
            ),
            InlineKeyboardButton(
                text='Изменить медиа', callback_data='edit_media'
            )
        ]
    ]
)

delete_media = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_create_msg'
            ),
            InlineKeyboardButton(
                text='Удалить медиа', callback_data='delete_media'
            )
        ]
    ]
)

edit_recipients_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Выбрать пресет', callback_data='choose_preset'
            ),
            InlineKeyboardButton(
                text='Настроить вручную', callback_data='custom_setting'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_create_msg'
            ),
            InlineKeyboardButton(
                text='На главную', callback_data='to_main'
            )
        ]
    ]
)

create_preset_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(
                text='Изменить название', callback_data='edit_preset_name'
            ),
            InlineKeyboardButton(
                text='Получатели', callback_data='preset_recipients'
            )
        ],
        [
            InlineKeyboardButton(
                text='Сохранить пресет', callback_data='save_preset'
            )
        ],
        [
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_manage_presets'
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

async def ready_presets_list():
    all_presets = await get_save_presets()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='return_to_recipients'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    keyboard.add(InlineKeyboardButton(text='Удалить текущий', callback_data='delete_current_preset'))
    keyboard.add(InlineKeyboardButton(text='Для всех ✔️', callback_data='preset_ALL'))
    for preset in all_presets:
        keyboard.add(
            InlineKeyboardButton(text=f'{str(preset.id)}. {preset.name}', callback_data=f"preset_{preset.preset_id}")
        )
    return keyboard.adjust(2, 1, 1, 3).as_markup()

async def presets_list():
    all_presets = await get_save_presets()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='return_to_sending_msg'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    keyboard.add(InlineKeyboardButton(text='Создать пресет', callback_data='create_preset'))
    keyboard.add(InlineKeyboardButton(text='Для всех ✔️', callback_data='preset-list_ALL'))
    for preset in all_presets:
        keyboard.add(
            InlineKeyboardButton(text=f'{preset.name}', callback_data=f"preset-list_{preset.preset_id}")
        )
    return keyboard.adjust(2, 1, 1, 3).as_markup()