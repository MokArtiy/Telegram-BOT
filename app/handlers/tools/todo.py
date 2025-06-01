import asyncio
import uuid
from datetime import datetime, timedelta
import dateparser
import logging

from aiogram import F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from dateutil.relativedelta import relativedelta

from ...database import requests as rq
from ...database.requests import check_ban_user
from ...database.models import RepeatInterval, Task
from ...keyboards import tools_kb
from ...states.states import ToDo
from ...utils import get_media as gm

scheduler = gm.scheduler

async def restore_notification():
    now = datetime.now()
    active_tasks = await rq.get_all_active_tasks()
     
    for task in active_tasks:
        try:
            if task.repeat_interval != RepeatInterval.NONE:
                new_notification = task.next_notification
                
                while new_notification and new_notification <= now:
                    new_notification = calculate_next_notification(
                        task.deadline,
                        task.repeat_interval,
                    )
                
                if new_notification:
                    await rq.task_update_next_notification(task_id=task.task_id, next_notification=new_notification)
                    update_task = await rq.set_task(task_id=task.task_id)
                    schedule_notification(task=update_task)
                else:
                    await rq.mark_task_overdue(task_id=update_task.task_id, overdue_check=True)
            
            elif task.next_notification and task.next_notification > now:
                schedule_notification(task=task)
            elif task.next_notification and task.next_notification <= now:
                await rq.mark_task_overdue(task_id=task.task_id, overdue_check=True)
        
        except Exception as e:
            logging.error(f"Ошибка восстановления задачи {task.task_id}: {e}")
            

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

async def input_none_value(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    current_state = await state.get_state()
    data = await state.get_data()
    task = await rq.get_unsave_task()
    none_key = 'ac13d5af-391a-40fe-bcb8-9b2095492d66'
    
    if current_state == ToDo.edit_name:
        await rq.task_update_name(task_id=task.task_id, task_name=none_key, user_id=callback.from_user.id)
        await gm.bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='✅ Успех! Название задачи успешно обновлено!'
            ),
            reply_markup=tools_kb.return_from_edit_task_kb
        )
        await state.clear()
    elif current_state == ToDo.edit_text:
        await rq.task_update_description_text(task_id=task.task_id, description_text=none_key)
        await gm.bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='✅ Успех! Текстовое описание было обновлено!'
            ),
            reply_markup=tools_kb.return_from_edit_description
        )
        await state.clear()
    elif current_state == ToDo.edit_media:
        await rq.task_update_description_media(task_id=task.task_id, description_media=none_key)
        await gm.bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='✅ Успех! Медиа задачи успешно обновлено!'
            ), 
            reply_markup=tools_kb.return_from_edit_description
        )
        await state.clear()

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
            caption='Введите новое название для задачи, не забывайте об ограничении в *100* символов!\n',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.return_from_input_name
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
                    caption='✅ Успех! Название задачи успешно обновлено!'
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
                    caption='❌ Название задачи не должно превышать *100* символов! Попробуйте снова...',
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
                caption='❌ Название должно содержать *только текст*! Попробуйте снова...',
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
                    f'*Текст:* {text}\n'
                    f'*Медиа:* {media}\n',
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
                caption='⚠️ Вы уже прикрепили кружок к сообщению! Хотите его удалить?',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.delete_description_media
        )
    elif task.description_media is not None and (task.description_media.split())[1] == 'voice':
        return await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='⚠️ Вы уже прикрепили гс к сообщению! Хотите его удалить?',
                parse_mode='markdown'
            ), 
            reply_markup=tools_kb.delete_description_media
        )
    else:
        await state.set_state(ToDo.edited_message_id)
        msg = await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='Отправьте текствое описание для вашей новой задачи',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.return_from_input_description
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
                    media=gm.Media_tg.tools_photo,
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
                message_id=data['edited_message_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.tools_photo,
                    caption='❌ Текст сообщения, *содержащего медиа-контент*, не должен превышать *1024* символа! Попробуйте снова...',
                    parse_mode='markdown'
                ),
                reply_markup=tools_kb.return_from_edit_description
            )
            elif len(message.text) > 4096 and task.description_media is None:
                await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['edited_message_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.tools_photo,
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

async def edit_media(callback: CallbackQuery, state: FSMContext):
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
            caption='Отправьте любое медиа к вашей новой задаче',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.return_from_input_description
    )
    await state.update_data(edited_message_id=msg.message_id)
    await state.set_state(ToDo.edit_media)

async def input_media(message: Message, state: FSMContext):
    task = await rq.get_unsave_task()
    if message.content_type == 'photo':
        data = await state.get_data()
        description_media = (message.photo[-1]).file_id + ' photo'
        await rq.task_update_description_media(task_id=task.task_id, description_media=description_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='✅ Успех! Медиа задачи успешно обновлено!'
            ), 
            reply_markup=tools_kb.return_from_edit_description
        )
        await state.clear()
    elif message.content_type == 'video':
        data = await state.get_data()
        description_media = message.video.file_id + ' video'
        await rq.task_update_description_media(task_id=task.task_id, description_media=description_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='✅ Успех! Медиа задачи успешно обновлено!'
            ), 
            reply_markup=tools_kb.return_from_edit_description
        )
        await state.clear()
    elif message.content_type == 'video_note':
        await state.update_data(edit_media=message.video_note.file_id + ' video_note')
        data = await state.get_data()
        if task.description_text is not None:
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['edited_message_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.tools_photo,
                    caption='⚠️ Вы пытаетесь создать сообщение с видео-кружком. У такого вида сообщений нету параметра *текст*!'
                            ' Удалите параметр *текст* или измените медиа файл!',
                    parse_mode='markdown'
                ), 
                reply_markup=tools_kb.delete_description_text
            )
        else:
            description_media = message.video_note.file_id + ' video_note'
            await rq.task_update_description_media(task_id=task.task_id, description_media=description_media)
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['edited_message_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.tools_photo,
                    caption='✅ Успех! Медиа задачи успешно обновлено!'
                ), 
                reply_markup=tools_kb.return_from_edit_description
            )
            await state.clear()
    elif message.content_type == 'audio':
        data = await state.get_data()
        description_media = message.audio.file_id + ' audio'
        await rq.task_update_description_media(task_id=task.task_id, description_media=description_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='✅ Успех! Медиа задачи успешно обновлено!'
            ), 
            reply_markup=tools_kb.return_from_edit_description
        )
        await state.clear()
    elif message.content_type == 'voice':
        await state.update_data(edit_media=message.voice.file_id + ' voice')
        data = await state.get_data()
        if task.description_text is not None:
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['edited_message_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.tools_photo,
                    caption='⚠️ Вы пытаетесь создать сообщение с гс. У такого вида сообщений нету параметра *текст*!'
                            ' Удалите параметр *текст* или измените медиа файл!',
                    parse_mode='markdown'
                ), 
                reply_markup=tools_kb.delete_description_text
            )
        else:
            description_media = message.voice.file_id + ' voice'
            await rq.task_update_description_media(task_id=task.task_id, description_media=description_media)
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['edited_message_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.tools_photo,
                    caption='✅ Успех! Медиа задачи успешно обновлено!'
                ), 
                reply_markup=tools_kb.return_from_edit_description
            )
            await state.clear()
    elif message.content_type == 'document':
        data = await state.get_data()
        description_media = message.document.file_id + ' document'
        await rq.task_update_description_media(task_id=task.task_id, description_media=description_media)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='✅ Успех! Медиа задачи успешно обновлено!'
            ), 
            reply_markup=tools_kb.return_from_edit_description
        )
        await state.clear()
    else:
        data = await state.get_data()
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='❌ Отправленное вами сообщение не подходит под обрабатываемые типы медиа! Попробуйте снова...',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.return_from_edit_description
        )
        
    await message.delete()
    
async def delete_description_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    task_id = (await rq.get_unsave_task()).task_id
    data = await state.get_data()
    await rq.task_update_description_media(task_id=task_id, description_media=data['edit_media'])
    await rq.task_delete_description_text()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='✅ Текст успешно удалён!'
        ),
        reply_markup=tools_kb.return_from_edit_description
    )
    await state.clear()
    
async def delete_description_media(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await rq.task_delete_description_media()
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='✅ Медиа успешно удалено!'
        ),
        reply_markup=tools_kb.return_from_edit_description
    )

async def show_description_msg(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    task = await rq.get_unsave_task()
    disable_notification = True
       
    await callback.answer('')
    await callback.message.delete()
    if task.description_media is not None:
        type_media = task.description_media.split(' ')[1]
        media_uid = task.description_media.split(' ')[0]
        if type_media == 'photo':
            await callback.message.answer_photo(
                photo=media_uid,
                caption=task.description_text,
                disable_notification=disable_notification,
                reply_markup=tools_kb.return_from_show_msg
            )
        elif type_media == 'video':
            await callback.message.answer_video(
                video=media_uid,
                caption=task.description_text,
                disable_notification=disable_notification,
                reply_markup=tools_kb.return_from_show_msg
            )
        elif type_media == 'video_note':
            await callback.message.answer_video_note(
                video_note=media_uid,
                disable_notification=disable_notification,
                reply_markup=tools_kb.return_from_show_msg
            )
        elif type_media == 'audio':
            await callback.message.answer_audio(
                audio=media_uid,
                caption=task.description_text,
                disable_notification=disable_notification,
                reply_markup=tools_kb.return_from_show_msg
            )
        elif type_media == 'voice':
            await callback.message.answer_voice(
                voice=media_uid,
                disable_notification=disable_notification,
                reply_markup=tools_kb.return_from_show_msg
            )
        elif type_media == 'document':
            await callback.message.answer_document(
                document=media_uid,
                caption=task.description_text,
                disable_notification=disable_notification,
                reply_markup=tools_kb.return_from_show_msg
            )
    else:
        await callback.message.answer(
            text=task.description_text,
            disable_notification=disable_notification,
            reply_markup=tools_kb.return_from_show_msg
        )
async def return_from_show_msg(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.delete()
    await state.clear()
    
    task = await rq.get_unsave_task()
    text = task.description_text if task.description_text is not None else '🚫'
    if len(text) > 450: text = '✔️'
    media = '✔️' if task.description_media is not None else '🚫'
    
    await callback.message.answer_photo(
        photo=gm.Media_tg.tools_photo,
        caption='Выберете действие ниже ⬇️\n\n'
                    f'*Текст:* {text}\n'
                    f'*Медиа:* {media}\n',
        parse_mode='markdown',
        reply_markup=tools_kb.todo_description_kb
    )
    
# INPUT DEADLINE
async def return_to_edit_deadline(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.clear()
    await callback.answer('')
    
    task = await rq.get_unsave_task()
    deadline = task.deadline if task.deadline is not None else '🚫'
    repeat_map = {
        RepeatInterval.NONE: "без повторения",
        RepeatInterval.HOURLY: "каждый час",
        RepeatInterval.DAILY: "каждый день",
        RepeatInterval.WEEKLY: "каждую неделю",
        RepeatInterval.MONTHLY: "каждый месяц"
    }
    repeat_interval = repeat_map.get(task.repeat_interval, "без повторения")
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Здесь вы можете задать сроки выполнения задачи.\nПеред началом редактирования рекомендуется ознакомиться с инструкцией 📖\n\n'
                    f'*Дата:* {deadline}\n'
                    f'*Повторение:* {repeat_interval}\n',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.task_deadline_kb
    )

async def edit_deadline(callback: CallbackQuery):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    
    task = await rq.get_unsave_task()
    deadline = task.deadline if task.deadline is not None else '🚫'
    repeat_map = {
        RepeatInterval.NONE: "без повторения",
        RepeatInterval.HOURLY: "каждый час",
        RepeatInterval.DAILY: "каждый день",
        RepeatInterval.WEEKLY: "каждую неделю",
        RepeatInterval.MONTHLY: "каждый месяц"
    }
    repeat_interval = repeat_map.get(task.repeat_interval, "без повторения")
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Здесь вы можете задать сроки выполнения задачи.\nПеред началом редактирования рекомендуется ознакомиться с инструкцией 📖\n\n'
                    f'*Дата:* {deadline}\n'
                    f'*Повторение:* {repeat_interval}\n',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.task_deadline_kb
    )
    
async def edit_date_and_time(callback: CallbackQuery, state: FSMContext):
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
            caption='Введите полную дату сроков задачи или воспользуйтесь готовыми шаблонами 🕐.\n'
                    '💡*Пример: * `31.05.2025 19:51`',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.patterns_deadline_kb
    )
    await state.update_data(edited_message_id=msg.message_id)
    await state.set_state(ToDo.input_date)

async def input_deadline(message: Message, state: FSMContext):
    try:
        task = await rq.get_unsave_task()
        text = message.text.lower()
        data = await state.get_data()  
        deadline = dateparser.parse(
            text, 
            languages=['ru'], 
            settings={
                'RELATIVE_BASE': datetime.now(),   # точка отсчёта для "понедельника", "завтра" и т.д.
                'PREFER_DATES_FROM': 'future',     # всегда брать будущие даты
                'DATE_ORDER': 'DMY',               # день-месяц-год (для явных дат)
            }
        )
        if not deadline:
            raise ValueError("Неверный формат даты")
        
        await rq.task_update_deadline(task_id=task.task_id, deadline=deadline.replace(microsecond=0))
        
        updated_task = await rq.get_unsave_task()
        if updated_task.repeat_interval is not None:
            await rq.task_update_next_notification(
                task_id=updated_task.task_id, next_notification=calculate_next_notification(deadline=updated_task.deadline, repeat_interval=updated_task.repeat_interval)
            )
        
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption=f'✅ Успех! Сроки задачи успешно обновлены!',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.return_from_input_date
        )
        await state.clear()
        await message.delete()
        
    except Exception as e:
        data = await state.get_data()
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption=f'❌ *Ошибка:* {e}. Попробуйте снова или обратитесь к [администратору](tg://user?id={5034740706}) бота.',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.patterns_deadline_kb
        )
        await message.delete()

async def deadline_today(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
        
    deadline = datetime.combine(datetime.today(), datetime.max.time())
    task = await rq.get_unsave_task()
    data = await state.get_data()
    
    await rq.task_update_deadline(task_id=task.task_id, deadline=deadline.replace(microsecond=0))
    
    updated_task = await rq.get_unsave_task()
    if updated_task.repeat_interval is not None:
        await rq.task_update_next_notification(
            task_id=updated_task.task_id, next_notification=calculate_next_notification(deadline=updated_task.deadline, repeat_interval=updated_task.repeat_interval)
        )
            
    await gm.bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption=f'✅ Успех! Сроки задачи успешно обновлены!',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.return_from_input_date
        )
    await state.clear()
    
async def deadline_tomorrow(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
        
    deadline = datetime.combine(datetime.today() + timedelta(days=1), datetime.max.time())
    task = await rq.get_unsave_task()
    data = await state.get_data()
    
    await rq.task_update_deadline(task_id=task.task_id, deadline=deadline.replace(microsecond=0))
    
    updated_task = await rq.get_unsave_task()
    if updated_task.repeat_interval is not None:
        await rq.task_update_next_notification(
            task_id=updated_task.task_id, next_notification=calculate_next_notification(deadline=updated_task.deadline, repeat_interval=updated_task.repeat_interval)
        )
    
    await gm.bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption=f'✅ Успех! Сроки задачи успешно обновлены!',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.return_from_input_date
        )
    await state.clear()

async def deadline_week(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
        
    deadline = datetime.combine(datetime.today() + timedelta(weeks=1), datetime.max.time())
    task = await rq.get_unsave_task()
    data = await state.get_data()
    
    await rq.task_update_deadline(task_id=task.task_id, deadline=deadline.replace(microsecond=0))
    
    updated_task = await rq.get_unsave_task()
    if updated_task.repeat_interval is not None:
        await rq.task_update_next_notification(
            task_id=updated_task.task_id, next_notification=calculate_next_notification(deadline=updated_task.deadline, repeat_interval=updated_task.repeat_interval)
        )
    
    await gm.bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption=f'✅ Успех! Сроки задачи успешно обновлены!',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.return_from_input_date
        )
    await state.clear()

async def task_repeat(callback: CallbackQuery, state: FSMContext):
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
            caption='Выберете интервал повторения уведомлений ⬇️.',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.repeat_deadline_kb
    )
    await state.update_data(edited_message_id=msg.message_id)

def calculate_next_notification(deadline: datetime, repeat_interval: RepeatInterval) -> datetime:
    now = datetime.now()
    if deadline > now:
        return deadline
    
    if repeat_interval == RepeatInterval.NONE:
        return None
    elif repeat_interval == RepeatInterval.HOURLY:
        next_date = deadline + timedelta(hours=(int((now - deadline).total_seconds()) // 3600) + 1)
    elif repeat_interval == RepeatInterval.DAILY:
        next_date = deadline + timedelta(days=((now.date() - deadline.date()).days) + 1)
    elif repeat_interval == RepeatInterval.WEEKLY:
        next_date = deadline + timedelta(weeks=((now.date() - deadline.date()).days // 7) + 1)
    elif repeat_interval == RepeatInterval.MONTHLY:
        months_passed = (now.year - deadline.year) * 12 + (now.month - deadline.month)
        next_date = deadline + relativedelta(months=+ (months_passed + 1))
    
    return next_date

async def process_repeat(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    
    repeat_map = {
        "without_repeat": RepeatInterval.NONE,
        "hourly_deadline": RepeatInterval.HOURLY,
        "daily_deadline": RepeatInterval.DAILY,
        "weakly_deadline": RepeatInterval.WEEKLY,
        "monthly_deadline": RepeatInterval.MONTHLY
    }
    repeat_interval = repeat_map.get(callback.data.lower(), RepeatInterval.NONE)
    task = await rq.get_unsave_task()
    data = await state.get_data()
    await rq.task_update_repeat_interval(task_id=task.task_id, repeat_interval=repeat_interval)
    
    update_task = await rq.get_unsave_task()
    await rq.task_update_next_notification(
        task_id=task.task_id, 
        next_notification=calculate_next_notification(deadline=update_task.deadline, repeat_interval=update_task.repeat_interval)
    )
    
    await gm.bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption=f'✅ Успех! Интервал повторения успешно обновлён!',
                parse_mode='markdown'
            ),
            reply_markup=tools_kb.return_from_input_date
        )
    await state.clear()
    
async def without_repeat(callback: CallbackQuery, state: FSMContext):
    await process_repeat(callback=callback, state=state)

async def hourly_deadline(callback: CallbackQuery, state: FSMContext):
    await process_repeat(callback=callback, state=state)
    
async def daily_deadline(callback: CallbackQuery, state: FSMContext):
    await process_repeat(callback=callback, state=state)

async def weakly_deadline(callback: CallbackQuery, state: FSMContext):
    await process_repeat(callback=callback, state=state)

async def monthly_deadline(callback: CallbackQuery, state: FSMContext):
    await process_repeat(callback=callback, state=state)
    
# SAVE TASK
async def save_task(callback: CallbackQuery):
    task = await rq.get_unsave_task()
    if (await rq.task_update_status(task_id=task.task_id) == 0):
        return await callback.answer('Сценарий задачи должен содержать название, текст/медиа и сроки выполнения!', show_alert=True)
    elif (await rq.task_update_status(task_id=task.task_id) == 1):
        await callback.answer('Задача успешно создана!', show_alert=True)

        schedule_notification(task=task)
        
        await callback.message.edit_media(
            InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='Это меню вашего персонального менеджера задач.\nВыберете действие ниже ⬇️', 
            ), 
            reply_markup=tools_kb.todo_main_kb
        )
        
def schedule_notification(task: Task):
    if task.next_notification:
        scheduler.add_job(
            send_task_notification,
            DateTrigger(run_date=task.next_notification),
            args=[task.user_id, task.task_id, task.name],
            misfire_grace_time=30
        )
    
    scheduler.add_job(
        send_daily_summary,
        CronTrigger(hour=9, minute=0),
        args=[task.user_id],
        misfire_grace_time=30
    )

async def send_task_notification(user_id: int, task_id: str, task_name: str):
    disable_notification = False
    task = await rq.set_task(task_id=task_id, user_id=user_id)
    if task.description_media is not None:
        type_media = task.description_media.split(' ')[1]
    else:
        type_media = 'text'
    try:
        await gm.bot.send_message(
            chat_id=user_id,
            text=f"⏰ *Напоминание:* пора выполнить задачу: {task_name}",
            parse_mode='markdown'
        )
        
        if type_media == 'photo':
            await gm.bot.send_photo(
                chat_id=user_id,
                photo=task.description_media.split(' ')[0],
                caption=task.description_text,
                disable_notification=disable_notification
            )
        elif type_media == 'video':
            await gm.bot.send_video(
                chat_id=user_id,
                video=task.description_media.split(' ')[0],
                caption=task.description_text,
                disable_notification=disable_notification
            )
        elif type_media == 'video_note':
            await gm.bot.send_video_note(
                chat_id=user_id,
                video_note=task.description_media.split(' ')[0],
                disable_notification=disable_notification
            )
        elif type_media == 'audio':
            await gm.bot.send_audio(
                chat_id=user_id,
                audio=task.description_media.split(' ')[0],
                caption=task.description_text,
                disable_notification=disable_notification
            )
        elif type_media == 'voice':
            await gm.bot.send_voice(
                chat_id=user_id,
                voice=task.description_media.split(' ')[0],
                disable_notification=disable_notification
            )
        elif type_media == 'document':
            await gm.bot.send_document(
                chat_id=user_id,
                document=task.description_media.split(' ')[0],
                caption=task.description_text,
                disable_notification=disable_notification
            )
        elif type_media == 'text':
            await gm.bot.send_message(
                chat_id=user_id,
                text=task.description_text,
                disable_notification=disable_notification
            )
        
        if task.repeat_interval != RepeatInterval.NONE:
            await rq.task_update_next_notification(
                task.task_id,
                next_notification=calculate_next_notification(task.deadline, task.repeat_interval)
            )
            task_update = await rq.set_task(task_id=task_id, user_id=user_id)
            if task_update.next_notification:
                schedule_notification(task=task_update)
    except Exception as e:
        logging.error(f"Ошибка в отправке уведомления о задаче: {e}")

async def send_daily_summary(user_id: int):
    try:
        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day)
        end_of_day = start_of_day + timedelta(days=1)
        
        tasks = await rq.get_task_daily(user_id=user_id, start_of_day=start_of_day, end_of_day=end_of_day)
        
        if tasks:
            task_list = "\n".join([f"• {task.name} ({task.deadline.strftime('%H:%M')})" for task in tasks])
            await gm.bot.send_message(
                chat_id=user_id,
                text=f'📅 Ваши задачи на сегодня:\n{task_list}'
            )
        else:
            await gm.bot.send_message(
                chat_id=user_id,
                text="🎉 У вас нет задач на сегодня!"
            )
    except Exception as e:
        logging.error(f'Ошибка в отправке утреннего уведомления: {e}')