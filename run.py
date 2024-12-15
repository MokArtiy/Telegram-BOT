import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv

from app.database.models import async_main
from app.utils.commands import set_commands
from app.handlers.start import get_start

load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await async_main()
    await set_commands(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
    
async def start_bot(bot: Bot):
    await bot.send_message(int(ADMIN_ID), text='Бот запущен')
    
    
dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
