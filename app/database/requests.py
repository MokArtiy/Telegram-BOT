from app.database.models import async_session
from app.database.models import User, Sending, Preset, Recipient, Task, ArchiveTask
from sqlalchemy import select, func

from datetime import datetime

from .models import RepeatInterval


#USER
async def set_user(tg_id: int, first_name: str, username: str = '') -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id, first_name=first_name, username=username))
            await session.commit()

async def get_users():
    async with async_session() as session:
        return await session.scalars(select(User))

async def get_banned_users():
    async with async_session() as session:
        return await session.scalars(select(User).where(User.banned == True))

async def check_ban_user(user_tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_tg_id))
        return user.banned

async def get_userlist_user(user_tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == user_tg_id))
    
async def update_user(user_tg_id, data):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_tg_id))
        
        if data.get('Description') != '':
            user.description = data.get('Description')
        if data.get('Phone Number') != '':
            user.phone_number = data.get('Phone Number')
        if data.get('Banned') != None:
            user.banned = data.get('Banned')
        
        await session.commit()

#MESSAGE
async def set_sending(sending_id: str):
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.sending_id == sending_id))
        
        if not sending:
            session.add(Sending(sending_id=sending_id))
            await session.commit()
            
        return await session.scalar(select(Sending).where(Sending.sending_id == sending_id))

async def update_sending_preset(sending_id: str, preset_id: str):
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.sending_id == sending_id))
        sending.sending_preset_id = preset_id
        await session.commit()

async def update_name(sending_id: str, sending_name: str):
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.sending_id == sending_id))
        if sending_name == 'None':
            sending.sending_name = None
        else:
            sending.sending_name = sending_name
        await session.commit()

async def update_text(sending_id: str, message_text: str):
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.sending_id == sending_id))
        if message_text == 'None':
            sending.message_text = None
        else:
            sending.message_text = message_text
        await session.commit()

async def update_media(sending_id: str, message_media: str):
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.sending_id == sending_id))
        if message_media == 'None':
            sending.message_media = None
        else:
            sending.message_media = message_media
        await session.commit()
        
async def update_status(sending_id: str) -> int:
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.sending_id == sending_id))
        if (sending.message_text is not None or sending.message_media is not None) and (sending.sending_name is not None) and (sending.sending_preset_id is not None):
            sending.sending_check = True
        else:
            return 0
        await session.commit()
        return 1
    
async def update_edit_status(sending_id: str, status: bool) -> None:
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.sending_id == sending_id))
        sending.edit_sending_check = status
        await session.commit()
        
async def get_unsave_sending(sending_id: str = None) -> Sending:
    async with async_session() as session:
        unsave_sending = await session.scalar(select(Sending).where(Sending.sending_check == False))
        
        if not unsave_sending:
            unsave_sending = await set_sending(sending_id=sending_id)
        return unsave_sending
    
async def get_save_sendings():
    async with async_session() as session:
        return await session.scalars(select(Sending).where(Sending.sending_check == True))
    
async def get_edit_current_sending():
    async with async_session() as session:
        return await session.scalar(select(Sending).where(Sending.edit_sending_check == True))

async def get_sending_preset_id(sending_id: str):
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.sending_id == sending_id))
        return sending.sending_preset_id
        
async def delete_text() -> None:
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.edit_sending_check == True))
        
        if not sending:
            sending = await session.scalar(select(Sending).where(Sending.sending_check == False))
            
        sending.message_text = None
        await session.commit()

async def delete_media() -> None:
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.edit_sending_check == True))
        
        if not sending:
            sending = await session.scalar(select(Sending).where(Sending.sending_check == False))

        sending.message_media = None
        await session.commit()

async def delete_sending(sending_id: str) -> None:
    async with async_session() as session:
        sending = await session.scalar(select(Sending).where(Sending.sending_id == sending_id))
        await session.delete(sending)
        await session.commit()

#PRESET
async def set_preset(preset_id: str):
    async with async_session() as session:
        preset = await session.scalar(select(Preset).where(Preset.preset_id == preset_id))
        
        if not preset:
            preset = session.add(Preset(preset_id=preset_id))
            await session.commit()
            
        return await session.scalar(select(Preset).where(Preset.preset_id == preset_id))
    
async def get_save_presets():
    async with async_session() as session:
        return await session.scalars(select(Preset).where(Preset.preset_check == True))
    
async def get_unsave_presets(preset_id: str = None) -> Preset:
    async with async_session() as session:
        unsave_preset = await session.scalar(select(Preset).where(Preset.preset_check == False))
        
        if not unsave_preset:
            unsave_preset = await set_preset(preset_id=preset_id)
        return unsave_preset
        
#RECIPIENTS

async def get_all_recipients_for_remove(sending_id: str, preset_id: str):
    async with async_session() as session:
        return await session.scalars(select(Recipient).where(Recipient.sending_id == sending_id and Recipient.preset_id == preset_id))
    
async def get_all_recipients_ids(sending_id: str, preset_id: str) -> dict[int, str]:
    async with async_session() as session:
        recipients = await session.scalars(select(Recipient).where(Recipient.sending_id == sending_id and Recipient.preset_id == preset_id))
        users_dict = {}
        
        for recipient in recipients:
            user_id = recipient.recipient_tg_id
            user_first_name = recipient.recipient_name
            
            users_dict[user_id] = f"{user_first_name}"
        
        return users_dict
    
async def get_recipients_sending(sending_id: str):
    async with async_session() as session:
        return await session.scalars(select(Recipient).where(Recipient.sending_id == sending_id))
    
async def get_recipients_preset(preset_id: str):
    async with async_session() as session:
        return await session.scalars(select(Recipient).where(Recipient.preset_id == preset_id))

async def add_recipient_all_preset(sending_id: str):
    async with async_session() as session:
        users = await get_users()
        for user in users:
            session.add(Recipient(recipient_tg_id=user.tg_id, recipient_name=user.first_name, 
                                  preset_id='ALL', sending_id=sending_id))
        await session.commit()
        
async def remove_current_preset(sending_id: str, preset_id: str):
    async with async_session() as session:
        recipients = await get_all_recipients_for_remove(sending_id=sending_id, preset_id=preset_id)
        sending = await session.scalar(select(Sending).where(Sending.sending_id == sending_id))
        for recipient in recipients:
            await session.delete(recipient)
        sending.sending_preset_id = None
        await session.commit()
        
#---------------------------------------------------
#TASKS TO-DO
#---------------------------------------------------

async def set_task(task_id: str, user_id: str = None):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
        
        if not task:
            count = await session.scalar(select(func.count()).select_from(Task).where(Task.user_id == user_id))
            task_name = f'Задача №{count + 1 if count != 0 else 1}'
            session.add(Task(task_id=task_id, user_id=user_id, name=task_name))
            await session.commit()
        
        return await session.scalar(select(Task).where(Task.task_id == task_id))

async def get_unsave_task(task_id: str = None, user_id: str = None) -> Task:
    async with async_session() as session:
        unsave_task = await session.scalar(select(Task).where(Task.task_check == False))
        
        if not unsave_task:
            unsave_task = await set_task(task_id=task_id, user_id=user_id)
        return unsave_task

async def get_task_by_id(task_id: str) -> Task:
    async with async_session() as session:
        return await session.scalar(select(Task).where(Task.task_id == task_id))
    
async def get_task_by_edit_check() -> Task:
    async with async_session() as session:
        return await session.scalar(select(Task).where(Task.edit_task_check == True))
    
async def task_update_name(task_id: str, task_name: str, user_id: str):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
        if task_name == 'ac13d5af-391a-40fe-bcb8-9b2095492d66':
            name_by_c = f'Задача №{await session.scalar(select(func.count()).select_from(Task).where(Task.user_id == user_id))}'
            task.name = name_by_c
        else:
            task.name = task_name
        await session.commit()
        
async def task_update_description_text(task_id: str, description_text: str):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
        if description_text == 'ac13d5af-391a-40fe-bcb8-9b2095492d66':
            task.description_text = None
        else:
            task.description_text = description_text
        await session.commit()
        
async def task_update_description_media(task_id: str, description_media: str):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
        if description_media == 'ac13d5af-391a-40fe-bcb8-9b2095492d66':
            task.description_media = None
        else:
            task.description_media = description_media
        await session.commit()

async def task_delete_description_text() -> None:
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.edit_task_check == True))
        
        if not task:
            task = await session.scalar(select(Task).where(Task.task_check == False))
        
        task.description_text = None
        await session.commit()

async def task_delete_description_media() -> None:
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.edit_task_check == True))
        
        if not task:
            task = await session.scalar(select(Task).where(Task.task_check == False))

        task.description_media = None
        await session.commit()

async def task_update_deadline(task_id: str, deadline: datetime) -> None:
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
            
        task.deadline = deadline
        await session.commit()
        
async def task_update_repeat_interval(task_id: str, repeat_interval: RepeatInterval) -> None:
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
            
        task.repeat_interval = repeat_interval
        await session.commit()

async def task_update_next_notification(task_id: str, next_notification: datetime) -> None:
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
            
        task.next_notification = next_notification
        await session.commit()
        
async def task_update_status(task_id: str) -> int:
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
        if(task.description_text is not None or task.description_media is not None) and (task.name is not None) and (task.deadline is not None):
            task.task_check = True
        else:
            return 0
        await session.commit()
        return 1

async def task_update_edit_check(task_id: str, edit_check: bool) -> None:
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
        
        task.edit_task_check = edit_check
        await session.commit()

async def task_update_completion(task_id: str, completion: bool) -> None:
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
            
        task.is_completed = completion
        await session.commit()

async def get_task_daily(user_id: int, start_of_day: datetime, end_of_day: datetime):
    async with async_session() as session:
        return await session.scalars(select(Task).where(
                    Task.user_id == user_id, 
                    Task.is_completed == False,
                    Task.deadline >= start_of_day,
                    Task.deadline < end_of_day))

async def get_all_active_tasks():
    async with async_session() as session:
        return await session.scalars(select(Task).where(Task.is_completed == False))
    
async def get_user_all_active_tasks(user_id: int):
    async with async_session() as session:
        return await session.scalars(select(Task).where(
            Task.user_id == user_id,
            Task.is_completed == False,
            Task.task_check == True))
    
async def mark_task_overdue(task_id: str, overdue_check: bool):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
        task.is_overdue = overdue_check
        await session.commit()
        
async def delete_task(task_id: str):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.task_id == task_id))
        await session.delete(task)
        await session.commit()
        
#Archive Task
async def set_archive_task(task_id: str, user_id: int, name: str, d_text: str,
                           d_media: str, deadline: datetime, repeat: RepeatInterval,
                           completion: bool):
    async with async_session() as session:
        session.add(ArchiveTask(
            task_id=task_id,
            user_id=user_id,
            name=name,
            description_text=d_text,
            description_media=d_media,
            deadline=deadline,
            repeat_interval=repeat,
            is_completed=completion
        ))
        await session.commit()