from aiogram.fsm.state import State, StatesGroup


class WorkGPT(StatesGroup):
    input_question = State()
    process = State()
    anecdote = State()
    
class InfAboutFriend(StatesGroup):
    gender = State()
    age = State()
    hobby = State()