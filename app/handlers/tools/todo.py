import asyncio
import uuid
from datetime import datetime

from aiogram import F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from ...database import requests as rq
from ...database.requests import check_ban_user
from ...keyboards import tools_kb
from ...states.states import ToDo
from ...utils import get_media as gm

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
                    f'*Текст:* `{text}`\n'
                    f'*Медиа:* `{media}`\n',
        parse_mode='markdown',
        reply_markup=tools_kb.todo_description_kb
    )
    
# INPUT DEADLINE
async def edit_deadline(callback: CallbackQuery, state: FSMContext):
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
            caption='Здесь вы можете задать сроки выполнения задачи. Перед началом редактирования рекомендуется ознакомиться с инструкцией 📖',
            parse_mode='markdown'
        ),
        reply_markup=tools_kb.task_deadline_kb
    )
