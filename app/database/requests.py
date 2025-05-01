from app.database.models import async_session
from app.database.models import User, Sending, Preset, Recipient
from sqlalchemy import select


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