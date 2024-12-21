import asyncio

from aiogram import F, html
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from ..AI.generation import generate_ai, generate_anecdote, generate_presents
from ..database.requests import check_ban_user
from ..keyboards import gpt_kb
from ..states.states import WorkGPT, InfAboutFriend


DATA = 0
TEXT: str


async def gpt_main_menu(callback: CallbackQuery):
    await callback.answer('')
    
    if (await check_ban_user(callback.from_user.id)):
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
        
    await callback.message.edit_text(
        text='Выберете, что вы хотите от ИИ', reply_markup=gpt_kb.gpt_main_kb
    )

async def stop(message: Message):
    await message.reply(text='Подождите, ваше сообщение генерируется...')
    
    
#CUSTOM-QUESTION
async def custom_question(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    if (await check_ban_user(callback.from_user.id)):
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.message.answer(text='Начните новый диалог, введя свой вопрос!')
    await state.set_state(WorkGPT.input_question)
    
async def stop_dialog(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    
    if (await check_ban_user(callback.from_user.id)):
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.message.answer(text='Выберете, что вы хотите от ИИ', reply_markup=gpt_kb.gpt_main_kb)

async def ai(message: Message, state: FSMContext):
    await state.set_state(WorkGPT.process)
    msg = await message.answer(text='Ответ генерируется...')
    res = await generate_ai(message.text)
    
    if res is not None:
        answer_q = res.choices[0].message.content
        try:
            await msg.delete()
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
    

#ANECDOTE
async def gen_more_anecdote(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    if (await check_ban_user(callback.from_user.id)):
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.set_state(WorkGPT.process)
    msg = await callback.message.edit_text(text='Анекдот генерируется...')
    res = await generate_anecdote()
    
    if res is not None:
        answer_q = res.choices[0].message.content
        try:
            await msg.delete()
            await callback.message.answer(answer_q, reply_markup=gpt_kb.next_anecdote_kb, parse_mode='markdown')
        except TelegramBadRequest as err:
            print(err)
            print(answer_q)
            await callback.message.answer(
                text='Ой-ой! Что-то пошло не так, попробуйте задать вопрос снова...',
                reply_markup=gpt_kb.next_anecdote_kb
            )
    else:
        await callback.message.answer(
            'Мои нейросети не могут ответить на ваш вопрос, попробуйте переформулировать задачу.',
            reply_markup=gpt_kb.next_anecdote_kb
        )
    await state.clear()
    
async def gen_anecdote(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    if (await check_ban_user(callback.from_user.id)):
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.set_state(WorkGPT.process)
    msg = await callback.message.answer(text='Анекдот генерируется...')
    res = await generate_anecdote()
    
    if res is not None:
        answer_q = res.choices[0].message.content
        try:
            await msg.delete()
            await callback.message.answer(answer_q, reply_markup=gpt_kb.next_anecdote_kb, parse_mode='markdown')
        except TelegramBadRequest as err:
            print(err)
            print(answer_q)
            await callback.message.answer(
                text='Ой-ой! Что-то пошло не так, попробуйте задать вопрос снова...',
                reply_markup=gpt_kb.next_anecdote_kb
            )
    else:
        await callback.message.answer(
            'Мои нейросети не могут ответить на ваш вопрос, попробуйте переформулировать задачу.',
            reply_markup=gpt_kb.next_anecdote_kb
        )
    await state.clear()


#PRESENT-FOR-FRIEND
async def gen_presents(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    if (await check_ban_user(callback.from_user.id)):
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.message.answer(text='Выберете пол вашего друга', reply_markup=gpt_kb.gender_kb)

async def men_fr(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    if (await check_ban_user(callback.from_user.id)):
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.update_data(gender='другу')
    await state.set_state(InfAboutFriend.age)
    await callback.message.answer(text='Сколько лет вашему другу?')
    
async def women_fr(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    if (await check_ban_user(callback.from_user.id)):
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.update_data(gender='подруге')
    await state.set_state(InfAboutFriend.age)
    await callback.message.answer(text='Сколько лет вашей подруге?')

async def age_fr(message: Message, state: FSMContext):
    try:
        a = int(message.text)
        if a > 0:
            await state.update_data(age=message.text)
            await state.set_state(InfAboutFriend.hobby)
            await message.answer(text='Опишите вашего друга/подругу, какой характер, хобби и т.д.')
        else:
            await message.answer(text='Такого возраста не существует...')
    except ValueError:
        await message.answer(text='Введите возраст цифрами')

async def hobby_fr(message: Message, state: FSMContext):
    await state.update_data(hobby=message.text)
    global DATA
    global TEXT
    DATA = await state.get_data()
    
    await state.set_state(WorkGPT.process)
    msg = await message.answer(text='Cписок подарков генерируется...')
    res = await generate_presents(gender=DATA["gender"], age=DATA["age"], hobby=DATA["hobby"])
    
    if res is not None:
        if DATA["gender"] == 'другу':
            TEXT = f'Вашему {DATA["age"]}-летнему другу, который {DATA["hobby"]}, может понравится:\n\n'
        else:
            TEXT = f'Вашей {DATA["age"]}-летней подруге, которая {DATA["hobby"]}, может понравится:\n\n'
        answer_q = TEXT + res.choices[0].message.content
        try:
            await msg.delete()
            await message.answer(answer_q, reply_markup=gpt_kb.next_presents_kb, parse_mode='markdown')
        except TelegramBadRequest as err:
            print(err)
            print(answer_q)
            await message.answer(
                text='Ой-ой! Что-то пошло не так, попробуйте задать вопрос снова...',
                reply_markup=gpt_kb.next_presents_kb
            )
    else:
        await message.answer(
            'Мои нейросети не могут ответить на ваш вопрос, попробуйте переформулировать задачу.',
            reply_markup=gpt_kb.next_presents_kb
        )
    await state.clear()

async def gen_more_presents(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    
    if (await check_ban_user(callback.from_user.id)):
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.set_state(WorkGPT.process)
    global DATA
    global TEXT
    msg = await callback.message.edit_text(text='Cписок подарков генерируется...')
    res = await generate_presents(gender=DATA["gender"], age=DATA["age"], hobby=DATA["hobby"])
    
    if res is not None:
        answer_q = TEXT + res.choices[0].message.content
        try:
            await msg.delete()
            await callback.message.answer(answer_q, reply_markup=gpt_kb.next_presents_kb, parse_mode='markdown')
        except TelegramBadRequest as err:
            print(err)
            print(answer_q)
            await callback.message.answer(
                text='Ой-ой! Что-то пошло не так, попробуйте задать вопрос снова...',
                reply_markup=gpt_kb.next_presents_kb
            )
    else:
        await callback.message.answer(
            'Мои нейросети не могут ответить на ваш вопрос, попробуйте переформулировать задачу.',
            reply_markup=gpt_kb.next_presents_kb
        )
    await state.clear()
