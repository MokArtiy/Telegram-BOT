import asyncio
import uuid

from aiogram import F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from ..database import requests as rq
from ..database.requests import check_ban_user
from ..keyboards import tools_kb
from ..states.states import ToDo
from ..utils import get_media as gm

async def return_to_tools(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.clear()
    await callback.answer('')
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Воспользуйтесь возможностями бота для решения любых задач!', 
        ), 
        reply_markup=tools_kb.tools_main_kb
    )

async def tools_main_menu(callback: CallbackQuery):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
        
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Воспользуйтесь возможностями бота для решения любых задач!', 
        ), 
        reply_markup=tools_kb.tools_main_kb
    )
    
#TO-DO
async def return_to_todo(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.clear()    
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Это меню вашего персонального менеджера задач.\nВыберете действие ниже ⬇️', 
        ), 
        reply_markup=tools_kb.todo_main_kb
    ) 

async def todo_main(callback: CallbackQuery):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Это меню вашего персонального менеджера задач.\nВыберете действие ниже ⬇️', 
        ), 
        reply_markup=tools_kb.todo_main_kb
    )

async def return_from_edit_task_kb(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
        
    await state.clear()
    await callback.answer('')
    
    task_id = str(uuid.uuid4())
    user_id = callback.from_user.id
    task = await rq.get_unsave_task(task_id=task_id, user_id=user_id)
    name = task.name if task.name is not None else '🚫'
    description = '✔️' if (task.description_text is not None) or (task.description_media is not None) else '🚫'
    deadline = '✔️' if task.deadline is not None else '🚫'
    status = 'сохранено' if task.task_check is True else 'не сохранено'
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption=f'Это меню добавления новых задач в ваш список дел.\nВыберете действие ниже ⬇️\n\n'
                    f'*Название:* {name}\n'
                    f'*Описание:* {description}\n'
                    f'*Дедлайн*: {deadline}\n'
                    f'*Статус*: {status}\n',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.todo_add_task_kb
    )

async def add_task(callback: CallbackQuery):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
        
    await callback.answer('')
    
    task_id = str(uuid.uuid4())
    user_id = callback.from_user.id
    task = await rq.get_unsave_task(task_id=task_id, user_id=user_id)
    name = task.name if task.name is not None else '🚫'
    description = '✔️' if (task.description_text is not None) or (task.description_media is not None) else '🚫'
    deadline = '✔️' if task.deadline is not None else '🚫'
    status = 'сохранено' if task.task_check is True else 'не сохранено'
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption=f'Это меню добавления новых задач в ваш список дел.\nВыберете действие ниже ⬇️\n\n'
                    f'*Название:* {name}\n'
                    f'*Описание:* {description}\n'
                    f'*Дедлайн*: {deadline}\n'
                    f'*Статус*: {status}\n',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.todo_add_task_kb
    )

#EDIT NAME TASK
async def edit_name_task(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await state.set_state(ToDo.edited_message_id)
    msg = await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Хорошо, отправьте мне новое название для вашей задачи, только не забывайте об ограничении в *100* символов!\n'
                    '```⚠️Примечение⚠️ Чтобы вернуть стандартное название - введите None```',
            parse_mode='markdown'
        )
    )
    await state.update_data(edited_message_id=msg.message_id)
    await state.set_state(ToDo.edit_name)
    
async def input_name_task(message: Message, state: FSMContext):
    task_id = (await rq.get_unsave_task()).task_id
    data = await state.get_data()
    
    if message.content_type == 'text':
        if len(message.text) <= 100:
            await rq.task_update_name(task_id=task_id, task_name=message.text, user_id=message.from_user.id)
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['edited_message_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.tools_photo,
                    caption='Успех! Название задачи успешно обновлено!'
                ),
                reply_markup=tools_kb.return_from_edit_task_kb
            )
            await state.clear()
        else:
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['edited_message_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.tools_photo,
                    caption='Название задачи не должно превышать *100* символов! Попробуйте снова...',
                    parse_mode='markdown'
                ),
                reply_markup=tools_kb.return_from_edit_task_kb
            )
    else:
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='Название должно содержать только текст! Попробуйте снова...',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.return_from_edit_task_kb
        )
    
    await message.delete()
    
#EDIT DESCRIPTION TASK
async def return_to_create_description(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.clear()
    await callback.answer('')
    
    task = await rq.get_unsave_task()
    text = task.description_text if task.description_text is not None else '🚫'
    if len(text) > 450: text = '✔️'
    media = '✔️' if task.description_media is not None else '🚫'
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Выберете действие ниже ⬇️\n\n'
                    f'*Текст:* {text}\n'
                    f'*Медиа:* {media}\n',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.todo_description_kb
    )

async def edit_description(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer(
        text='⚠️ СПРАВКА ⚠️\n\nОписание задачи может представлять из себя как комбинацию текста (до 1024 символов) '
             'с одним любым медиа, так и просто текст (до 4096 символов).',
        show_alert=True
        )
    
    task = await rq.get_unsave_task()
    text = task.description_text if task.description_text is not None else '🚫'
    if len(text) > 450: text = '✔️'
    media = '✔️' if task.description_media is not None else '🚫'
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Выберете действие ниже ⬇️\n\n'
                    f'*Текст:* `{text}`\n'
                    f'*Медиа:* `{media}`\n',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.todo_description_kb
    )

async def edit_text(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    task = await rq.get_unsave_task()
    if task.description_media is not None and (task.description_media.split())[1] == 'video_note':
        await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='Вы уже прикрепили кружок к сообщению! Хотите его удалить?',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.delete_media
        )
    elif task.description_media is not None and (task.description_media.split())[1] == 'voice':
        return await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='Вы уже прикрепили гс к сообщению! Хотите его удалить?',
                parse_mode='markdown'
            ), 
            reply_markup=tools_kb.delete_media
        )
    else:
        await state.set_state(ToDo.edited_message_id)
        msg = await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='Хорошо, отправьте мне текствое описание для вашей новой задачи',
                parse_mode='markdown'
            )
        )
        await state.update_data(edited_message_id=msg.message_id)
        await state.set_state(ToDo.edit_text)

async def input_text(message: Message, state: FSMContext):
    task = await rq.get_unsave_task()
    
    if message.content_type == 'text':
        if (len(message.text) <= 1024 and task.description_media is not None) or (len(message.text) <= 4096 and task.description_media is None):
            data = await state.get_data()
            await rq.task_update_description_text(task_id=task.task_id, description_text=message.text)
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['edited_message_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='✅ Успех! Текстовое описание было обновлено!'
                ),
                reply_markup=tools_kb.return_from_edit_description
            )
            await state.clear()
        else:
            data = await state.get_data()
            if len(message.text) > 1024 and task.description_media is not None:
                await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_admin_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='❌ Текст сообщения, *содержащего медиа-контент*, не должен превышать *1024* символа! Попробуйте снова...',
                    parse_mode='markdown'
                ),
                reply_markup=tools_kb.return_from_edit_description
            )
            elif len(message.text) <= 4096 and task.description_media is None:
                await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_admin_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.admin_photo,
                    caption='❌ Текст сообщения *без медиа-контента* не должен превышать *4096* символов! Попробуйте снова...',
                    parse_mode='markdown'
                ),
                reply_markup=tools_kb.return_from_edit_description
            )
    else:
        data = await state.get_data()
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='❌ *Текстовое* описание должно содержать только *текст*! Это же логично блин...',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.return_from_edit_description
        )
        
    await message.delete()
    
    #К окну ввода текста добавить кнопки - назад - на главную - "None", то же самое проделать и с другими окнами