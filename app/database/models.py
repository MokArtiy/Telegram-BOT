from sqlalchemy import BigInteger, DateTime, String, ForeignKey, Enum as SqlEnum, func
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from aiogram.types import contact

import os
from dotenv import load_dotenv
from datetime import datetime
from enum import Enum

load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True, default=None)
    description: Mapped[str] = mapped_column(String(70), nullable=True, default=None)
    banned: Mapped[bool] = mapped_column(default=False, nullable=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Sending(Base):
    __tablename__ = 'sending'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sending_id: Mapped[str] = mapped_column(nullable=False)
    sending_preset_id: Mapped[str] = mapped_column(nullable=True, default=None)
    sending_name: Mapped[str] = mapped_column(String(32), nullable=True, default=None)
    sending_check: Mapped[bool] = mapped_column(nullable=False, default=False)
    edit_sending_check: Mapped[bool] = mapped_column(nullable=False, default=False)
    sending_time: Mapped[str] = mapped_column(nullable=True, default=None)
    message_text: Mapped[str] = mapped_column(String(1024), nullable=True, default=None)
    message_media: Mapped[str] = mapped_column(nullable=True, default=None)

class Recipient(Base):
    __tablename__ = 'recipient'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recipient_tg_id = mapped_column(BigInteger, nullable=False)
    recipient_name: Mapped[str] = mapped_column(nullable=False)
    preset_id: Mapped[str] = mapped_column(nullable=False, default=None)
    sending_id: Mapped[str] = mapped_column(nullable=False, default=None)
    
    
class Preset(Base):
    __tablename__ = 'preset'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    preset_id: Mapped[int] = mapped_column(nullable=False)
    preset_check: Mapped[bool] = mapped_column(nullable=False, default=False)
    preset_name: Mapped[str] = mapped_column(String(32), nullable=True, default=None)

# ToDo
class RepeatInterval(str, Enum):
    NONE = "none"
    DAILY = "dayly"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class Task(Base):
    __tablename__ = 'task'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(nullable=False)
    user_id = mapped_column(BigInteger, ForeignKey('user.tg_id'), nullable=False)
    task_check: Mapped[bool] = mapped_column(nullable=False, default=False)
    edit_task_check: Mapped[bool] = mapped_column(nullable=False, default=False)
    name: Mapped[str] = mapped_column(String(100), nullable=True, default=None)
    description_text: Mapped[str] = mapped_column(String(4097), nullable=True, default=None)
    description_media: Mapped[str] = mapped_column(nullable=True, default=None)
    deadline: Mapped[datetime] = mapped_column(nullable=True, default=None)
    repeat_interval: Mapped[RepeatInterval] = mapped_column(SqlEnum(RepeatInterval), default=RepeatInterval.NONE)
    next_notification: Mapped[datetime] = mapped_column(nullable=True, default=None)
    is_completed: Mapped[bool] = mapped_column(nullable=False, default=False)
    user: Mapped["User"] = relationship(back_populates="tasks")

#DB-FUNCTIONS
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)