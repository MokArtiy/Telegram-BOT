from app.database.models import async_session
from app.database.models import User
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
        