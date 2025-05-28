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
    description = task.description if task.description is not None else '🚫'
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
    description = task.description if task.description is not None else '🚫'
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
async def edit_description_task(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_data(ToDo.edited_message_id)
    msg = await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.tools_photo,
            caption='Хорошо, отправьте мне новое описание вашей задачи. На вход принимаются текст до *1024* символов, '
                    'голосовые сообщения, аудио сообщения, фотографии, документы, кружки и видео сообщения.\n'
                    '```⚠️Примечение⚠️ Чтобы сделать описание пустым - введите None```',
            parse_mode='markdown'
        )
    )
    await state.update_data(edited_message_id=msg.message_id)
    await state.set_state(ToDo.edit_description)

async def input_description(message: Message, state: FSMContext):
    task = await rq.get_unsave_task()
    if message.content_type == 'photo':
        data = await state.get_data()
        description = (message.photo[-1]).file_id + ' photo'
        await rq.task_update_description(task_id=task.task_id, description=description)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='Успех! Описание задачи успешно обновлено!'
            ),
            reply_markup=tools_kb.return_from_edit_task_kb
        )
        await state.clear()
    elif message.content_type == 'video':
        data = await state.get_data()
        description = message.video.file_id + ' video'
        await rq.task_update_description(task_id=task.task_id, description=description)
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['edited_message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.tools_photo,
                caption='Успех! Описание задачи успешно обновлено!'
            ),
            reply_markup=tools_kb.return_from_edit_task_kb
        )
    #elif message.content_type == 'video_note':
        
#  Описание переходит на клавиатуру изменения текста и медиа, внизу кнопка показать текущее сообщение, ниже "назад" и "на главную"