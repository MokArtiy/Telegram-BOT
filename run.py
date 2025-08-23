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
from app.handlers.tools import tools, todo
from app.utils.commands import set_commands
from app.utils import get_media as gm
from app.handlers import start, gpt_tasks, admin_panel, input_key, my_profile, support
from app.states.states import WorkGPT, InfAboutFriend, SecretKey, AdminPanel, ToDo


load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
PARAM = ''

# print("Токен из переменных окружения:", os.environ.get('TOKEN'))
# print("Токен из .env:", os.getenv('TOKEN'))

bot = Bot(token=TOKEN, 
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
dp = Dispatcher()
scheduler = gm.scheduler

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
    
    scheduler.start()
    
async def stop_bot(bot: Bot):
    await bot.send_message(int(ADMIN_ID), text='Бот выключен')
    

dp.startup.register(start_bot)
dp.shutdown.register(stop_bot)
dp.message.register(start.get_start, Command(commands='start'))
#dp.message.register(start.photo_inf, F.photo)
dp.callback_query.register(start.to_main, F.data == 'to_main')

#gpt-functions
dp.callback_query.register(gpt_tasks.gpt_main_menu, F.data == 'gpt')
dp.message.register(gpt_tasks.stop, WorkGPT.process)
#CUSTOM-QUESTION
dp.callback_query.register(gpt_tasks.custom_question, F.data == 'custom_question')   
dp.callback_query.register(gpt_tasks.more_question, F.data == 'more_question')
dp.callback_query.register(gpt_tasks.stop_dialog, F.data == 'stop_dialog')
dp.callback_query.register(gpt_tasks.stop_dialog_in_ai, F.data == 'stop_dialog_in_ai')
dp.callback_query.register(gpt_tasks.to_main_from_ai, F.data == 'to_main_from_ai')
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
dp.callback_query.register(admin_panel.return_to_sending_msg, F.data == 'return_to_sending_msg')
dp.callback_query.register(admin_panel.admin_main_menu, F.data == 'admin_panel')
dp.callback_query.register(admin_panel.admin_users_list, F.data == 'users_list')
dp.callback_query.register(admin_panel.get_list_banned_users, F.data == 'ban_users')
dp.callback_query.register(admin_panel.get_user, F.data.startswith('user_'))
dp.callback_query.register(admin_panel.get_banned_user, F.data.startswith('bans_'))
dp.callback_query.register(admin_panel.bun_user, F.data == 'ban_user')
dp.callback_query.register(admin_panel.unban_user, F.data == 'unban_user')
dp.callback_query.register(admin_panel.unban_user_in_ban, F.data == 'unban_user_in_ban')
dp.callback_query.register(admin_panel.bun_user_in_ban, F.data == 'ban_user_in_ban')
#SENDING-MESSAGE
dp.callback_query.register(admin_panel.return_to_create_msg, F.data == 'return_to_create_msg')
dp.callback_query.register(admin_panel.sending_msg, F.data == 'sending_msg')
dp.callback_query.register(admin_panel.create_sending, F.data == 'create_sending')
dp.callback_query.register(admin_panel.edit_name, F.data == 'edit_name')
dp.callback_query.register(admin_panel.edit_text, F.data == 'edit_text')
dp.callback_query.register(admin_panel.edit_media, F.data == 'edit_media')
dp.callback_query.register(admin_panel.delete_text, F.data == 'delete_text')
dp.callback_query.register(admin_panel.delete_media, F.data == 'delete_media')
dp.message.register(admin_panel.input_name, AdminPanel.edit_name)
dp.message.register(admin_panel.input_text, AdminPanel.edit_text)
dp.message.register(admin_panel.input_media, AdminPanel.edit_media)
#presets
dp.callback_query.register(admin_panel.return_to_recipients, F.data == 'return_to_recipients')
dp.callback_query.register(admin_panel.return_to_manage_presets, F.data == 'return_to_manage_presets')
dp.callback_query.register(admin_panel.edit_recipients, F.data == 'edit_recipients')
dp.callback_query.register(admin_panel.choose_preset, F.data == 'choose_preset')
dp.callback_query.register(admin_panel.delete_current_preset, F.data == 'delete_current_preset')
dp.callback_query.register(admin_panel.manage_presets, F.data == 'manage_presets')
dp.callback_query.register(admin_panel.create_preset, F.data == 'create_preset')
dp.callback_query.register(admin_panel.choose_save_preset, F.data.startswith('preset-save-list_'))
#manage sending
dp.callback_query.register(admin_panel.save_sending, F.data == 'save_and_create_sending')
dp.callback_query.register(admin_panel.manage_sending, F.data == 'manage_sending')
dp.callback_query.register(admin_panel.return_to_manage_sending, F.data == 'return_to_manage_sending')
dp.callback_query.register(admin_panel.return_to_manage_current_sending, F.data == 'return_to_manage_current_sending')
dp.callback_query.register(admin_panel.return_to_edit_current_sending, F.data == 'return_to_edit_current_sending')
dp.callback_query.register(admin_panel.return_to_current_sending_recipients, F.data == 'return_to_current_sending_recipients')
dp.callback_query.register(admin_panel.run_sending, F.data == 'run_sending')
dp.callback_query.register(admin_panel.edit_current_sending, F.data == 'edit_current_sending')
dp.callback_query.register(admin_panel.edit_current_sending_name, F.data == 'edit_current_sending_name')
dp.callback_query.register(admin_panel.edit_current_sending_text, F.data == 'edit_current_sending_text')
dp.callback_query.register(admin_panel.edit_current_sending_media, F.data == 'edit_current_sending_media')
dp.callback_query.register(admin_panel.edit_current_sending_recipients, F.data == 'edit_current_sending_recipients')
dp.callback_query.register(admin_panel.choose_current_sending_preset, F.data == 'choose_current_sending_preset')
dp.callback_query.register(admin_panel.delete_current_preset_in_current_sending, F.data == 'delete_current_preset_in_current_sending')
dp.callback_query.register(admin_panel.delete_current_sending, F.data == 'delete_current_sending')
dp.callback_query.register(admin_panel.yes_delete, F.data == 'yes_delete')
dp.callback_query.register(admin_panel.no_delete, F.data == 'no_delete')
dp.message.register(admin_panel.input_current_sending_name, AdminPanel.edit_current_sending_name)
dp.message.register(admin_panel.input_current_sending_text, AdminPanel.edit_current_sending_text)
dp.message.register(admin_panel.input_current_sending_media, AdminPanel.edit_current_sending_media)
dp.callback_query.register(admin_panel.manage_current_sending, F.data.startswith('sending-list_'))
dp.callback_query.register(admin_panel.choose_save_preset_in_current_sending, F.data.startswith('preset-save-list-current-sending_'))

#input-key
dp.callback_query.register(input_key.to_main_from_gift, F.data == 'to_main_from_gift')
dp.callback_query.register(input_key.return_to_key, F.data == 'return_to_key')
dp.callback_query.register(input_key.return_to_key_from_gift, F.data == 'return_to_key_from_gift')
dp.callback_query.register(input_key.secret_key_main, F.data == 'secret_key')
dp.callback_query.register(input_key.input_key, F.data == 'input_key')
dp.callback_query.register(input_key.get_gift, F.data == 'get_gift')
dp.message.register(input_key.check_key, SecretKey.input_key)

#tools
dp.callback_query.register(tools.return_to_tools, F.data == 'return_to_tools')
dp.callback_query.register(tools.tools_main_menu, F.data == 'utils')

#todo
dp.callback_query.register(todo.return_to_todo, F.data == 'return_to_todo')
dp.callback_query.register(todo.return_from_edit_task_kb, F.data == 'return_to_create_task')
dp.callback_query.register(todo.return_to_create_description, F.data == 'return_to_create_description')
dp.callback_query.register(todo.return_to_edit_deadline, F.data == 'return_to_edit_deadline')
dp.callback_query.register(todo.todo_main, F.data == 'todo_main')
dp.callback_query.register(todo.add_task, F.data == 'add_task')
dp.callback_query.register(todo.input_none_value_task, F.data == 'input_none_value_task')
dp.callback_query.register(todo.edit_name_task, F.data == 'task_name')
dp.callback_query.register(todo.edit_description, F.data == 'task_description')
dp.callback_query.register(todo.edit_text, F.data == 'description_caption')
dp.callback_query.register(todo.edit_media, F.data == 'description_media')
dp.callback_query.register(todo.delete_description_text, F.data == 'delete_description_text')
dp.callback_query.register(todo.delete_description_media, F.data == 'delete_description_media')
dp.callback_query.register(todo.show_description_task_msg, F.data == 'show_description_task_msg')
dp.callback_query.register(todo.return_from_show_msg, F.data == 'return_from_show_msg')
dp.callback_query.register(todo.edit_deadline, F.data == 'task_deadline')
dp.callback_query.register(todo.edit_date_and_time, F.data == 'date_and_time')
dp.callback_query.register(todo.deadline_today, F.data == 'deadline_today')
dp.callback_query.register(todo.deadline_tomorrow, F.data == 'deadline_tomorrow')
dp.callback_query.register(todo.deadline_week, F.data == 'deadline_week')
dp.callback_query.register(todo.task_repeat, F.data == 'task_repeat')
dp.callback_query.register(todo.without_repeat, F.data == 'without_repeat')
dp.callback_query.register(todo.hourly_deadline, F.data == 'hourly_deadline')
dp.callback_query.register(todo.daily_deadline, F.data == 'daily_deadline')
dp.callback_query.register(todo.weakly_deadline, F.data == 'weakly_deadline')
dp.callback_query.register(todo.monthly_deadline, F.data == 'monthly_deadline')
dp.callback_query.register(todo.save_task, F.data == 'task_save')
#current tasks
dp.callback_query.register(todo.current_tasks, F.data == 'current_tasks')
dp.callback_query.register(todo.return_to_current_tasks, F.data == 'return_to_current_tasks')
dp.callback_query.register(todo.complete_current_task, F.data == 'complete_current_task')
dp.callback_query.register(todo.edit_current_task, F.data == 'edit_current_task')
dp.callback_query.register(todo.return_to_current_task, F.data == 'return_to_current_task')
dp.callback_query.register(todo.return_to_current_edit_task, F.data == 'return_to_current_edit_task')
dp.callback_query.register(todo.edit_current_task_name, F.data == 'edit_current_task_name')
dp.callback_query.register(todo.none_value_current_task, F.data == 'none_value_current_task')
dp.callback_query.register(todo.edit_current_task_description, F.data == 'edit_current_task_description')
dp.callback_query.register(todo.show_editing_description_msg, F.data == 'show_editing_description_msg')
dp.callback_query.register(todo.return_from_editing_msg, F.data == 'return_from_editing_msg')
dp.callback_query.register(todo.editing_description_caption, F.data == 'editing_description_caption')
dp.callback_query.register(todo.editing_description_media, F.data == 'editing_description_media')
dp.callback_query.register(todo.delete_current_description_text, F.data == 'delete_current_description_text')
dp.callback_query.register(todo.delete_current_description_media, F.data == 'delete_current_description_media')
dp.callback_query.register(todo.edit_current_task_deadline, F.data == 'edit_current_task_deadline')
dp.callback_query.register(todo.editing_date_and_time, F.data == 'editing_date_and_time')
dp.callback_query.register(todo.return_to_editing_deadline, F.data == 'return_to_editing_deadline')
dp.callback_query.register(todo.show_current_task, F.data.startswith('current-preset_'))

dp.message.register(todo.input_media_task, ToDo.edit_media)
dp.message.register(todo.input_text_task, ToDo.edit_text)
dp.message.register(todo.input_name_task, ToDo.edit_name)
dp.message.register(todo.input_deadline, ToDo.input_date)

dp.message.register(todo.input_current_task_name, ToDo.edit_current_task_name)
dp.message.register(todo.input_current_task_text, ToDo.edit_current_task_text)
dp.message.register(todo.input_current_task_media, ToDo.edit_current_task_media)
#plug
dp.callback_query.register(support.plug, F.data == 'support_team')
dp.callback_query.register(my_profile.plug, F.data == 'my_profile')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
