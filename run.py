import os
import asyncio
import logging
from dotenv import load_dotenv
from sys import argv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.database.models import create_db, drop_db, async_session
from app.utils.commands import set_commands
from app.handlers import start, gpt_tasks, admin_panel
from app.states.states import WorkGPT, InfAboutFriend


load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
PARAM = ''

bot = Bot(token=TOKEN, 
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
dp = Dispatcher()

async def main():
    global PARAM
    PARAM = argv
    if len(PARAM) != 2 :
        PARAM.append('create')
        
    await set_commands(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
    
async def start_bot(bot: Bot):
    if PARAM[1]=='drop':
        await drop_db()
    await create_db()
    
    await bot.send_message(int(ADMIN_ID), text='Бот запущен')
    
async def stop_bot(bot: Bot):
    await bot.send_message(int(ADMIN_ID), text='Бот выключен')
    

dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)
dp.message.register(start.get_start, Command(commands='start'))
dp.callback_query.register(start.to_main, F.data == 'to_main')

#gpt-functions
dp.callback_query.register(gpt_tasks.gpt_main_menu, F.data == 'gpt')
dp.message.register(gpt_tasks.stop, WorkGPT.process)
#CUSTOM-QUESTION
dp.callback_query.register(gpt_tasks.custom_question, F.data == 'custom_question')
dp.callback_query.register(gpt_tasks.stop_dialog, F.data == 'stop_dialog')
dp.message.register(gpt_tasks.ai, WorkGPT.input_question)
#ANECDOTE
dp.callback_query.register(gpt_tasks.gen_anecdote, F.data == 'anecdote')
dp.callback_query.register(gpt_tasks.gen_more_anecdote, F.data == 'more_anecdote')
#PRESENTS
dp.callback_query.register(gpt_tasks.gen_presents, F.data == 'present_4_friend')
dp.callback_query.register(gpt_tasks.men_fr, F.data == 'men_fr')
dp.callback_query.register(gpt_tasks.women_fr, F.data == 'women_fr')
dp.message.register(gpt_tasks.age_fr, InfAboutFriend.age)
dp.message.register(gpt_tasks.hobby_fr, InfAboutFriend.hobby)
dp.callback_query.register(gpt_tasks.gen_more_presents, F.data == 'more_presents')

#admin-panel
dp.callback_query.register(admin_panel.return_to_panel, F.data == 'return_to_panel')
dp.callback_query.register(admin_panel.return_to_list, F.data == 'return_to_list')
dp.callback_query.register(admin_panel.return_to_ban_list, F.data == 'return_to_ban_list')
dp.callback_query.register(admin_panel.admin_main_menu, F.data == 'admin_panel')
dp.callback_query.register(admin_panel.admin_users_list, F.data == 'users_list')
dp.callback_query.register(admin_panel.get_list_banned_users, F.data == 'ban_users')
dp.callback_query.register(admin_panel.get_user, F.data.startswith('user_'))
dp.callback_query.register(admin_panel.get_banned_user, F.data.startswith('bans_'))
dp.callback_query.register(admin_panel.bun_user, F.data == 'ban_user')
dp.callback_query.register(admin_panel.unban_user, F.data == 'unban_user')
dp.callback_query.register(admin_panel.unban_user_in_ban, F.data == 'unban_user_in_ban')
dp.callback_query.register(admin_panel.bun_user_in_ban, F.data == 'ban_user_in_ban')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
