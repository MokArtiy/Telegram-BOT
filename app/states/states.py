from aiogram.fsm.state import State, StatesGroup


class WorkGPT(StatesGroup):
    input_question = State()
    process = State()
    anecdote = State()
    message_gpt_id = State()
    
class InfAboutFriend(StatesGroup):
    gender = State()
    age = State()
    hobby = State()
    
class AdminPanel(StatesGroup):
    check_user = State()
    message_admin_id = State()
    edit_name = State()
    edit_text = State()
    edit_media = State()
    chosen_preset = State()
    current_sending_id = State()
    edit_current_sending_name = State()
    edit_current_sending_text = State()
    edit_current_sending_media = State()
        
class SecretKey(StatesGroup):
    input_key = State()
    message_id = State()
    
class ToDo(StatesGroup):
    edited_message_id = State()
    edit_name = State()
    edit_text = State()
    edit_media = State()
    input_date = State()