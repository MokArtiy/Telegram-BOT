import os
import asyncio
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.database.models import async_main
from app.utils.commands import set_commands
from app.handlers.start import get_start
from app.handlers import gpt_tasks
from app.states.states import WorkGPT

load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

bot = Bot(token=TOKEN, 
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
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

#gpt-functions
dp.callback_query.register(gpt_tasks.to_main, F.data == 'to_main')
dp.callback_query.register(gpt_tasks.gpt_main_menu, F.data == 'gpt')
dp.callback_query.register(gpt_tasks.custom_question, F.data == 'custom_question')
dp.callback_query.register(gpt_tasks.stop_dialog, F.data == 'stop_dialog')
dp.message.register(gpt_tasks.ai, WorkGPT.input_question)
dp.message.register(gpt_tasks.stop, WorkGPT.process)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
