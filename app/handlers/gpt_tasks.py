from aiogram import F, html
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from ..AI.generation import generate
from ..keyboards import main_kb, gpt_kb
from ..states.states import WorkGPT 


async def to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.edit_text(
        text=f"Добро пожаловать в {html.link('NewYear-Bot', 'https://t.me/new_artem_year_bot')}\n"
             f"Выберете, что вы хотите сделать в меню ниже ⬇️",
        reply_markup=main_kb.main_menu_1(callback.from_user.id)
    )

async def gpt_main_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        text='Выберете, что вы хотите от ИИ', reply_markup=gpt_kb.gpt_main_kb
    )
    
async def custom_question(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer(text='Начните новый диалог, введя свой вопрос!')
    await state.set_state(WorkGPT.input_question)

async def stop(message: Message):
    await message.answer(text='Подождите, ваше сообщение генерируется...')
    
async def stop_dialog(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.answer(text='Выберете, что вы хотите от ИИ', reply_markup=gpt_kb.gpt_main_kb)

async def ai(message: Message, state: FSMContext):
    await state.set_state(WorkGPT.process)
    await message.answer(text='Ответ генерируется...')
    res = await generate(message.text)
    
    if res is not None:
        answer_q = res.choices[0].message.content
        try:
            await message.answer(answer_q, reply_markup=gpt_kb.next_kb, parse_mode='markdown')
        except TelegramBadRequest as err:
            print(err)
            print(answer_q)
            await message.answer(
                'Ой-ой! Что-то пошло не так, попробуйте переформулировать вопрос или напишите позже...',
                reply_markup=gpt_kb.next_kb
            )
    else:
        await message.answer(
            'Мои нейросети не могут ответить на ваш вопрос, попробуйте переформулировать задачу.',
            reply_markup=gpt_kb.next_kb
        )
    await state.set_state(WorkGPT.input_question)


