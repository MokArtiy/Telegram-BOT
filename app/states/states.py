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
    edit_text = State()
    edit_media = State()
    chosen_preset = State()
        
class SecretKey(StatesGroup):
    input_key = State()
    message_id = State()