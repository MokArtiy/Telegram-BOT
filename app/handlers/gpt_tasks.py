import asyncio

from aiogram import F, html
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from ..AI.generation import generate_ai, generate_anecdote, generate_presents
from ..database.requests import check_ban_user
from ..keyboards import gpt_kb, main_kb
from ..states.states import WorkGPT, InfAboutFriend
from ..utils import get_media as gm


DATA = 0
TEXT: str


async def gpt_main_menu(callback: CallbackQuery):  
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Выберете, что вы хотите от ИИ', 
        ), 
        reply_markup=gpt_kb.gpt_main_kb
    )

async def stop(message: Message):
    await message.reply(text='Подождите, ваше сообщение генерируется...')
    
    
#CUSTOM-QUESTION
async def custom_question(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await state.set_state(WorkGPT.message_gpt_id)
    msg = await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Начните новый диалог, введя свой вопрос!'
        )
    )
    await state.update_data(message_gpt_id=msg.message_id)
    await state.set_state(WorkGPT.input_question)
    
async def more_question(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    data = await state.get_data()
    await state.set_state(WorkGPT.message_gpt_id)
    msg = await gm.bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=data['message_gpt_id'],
        media = InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Начните новый диалог, введя свой вопрос!'
        )
    )
    await callback.message.delete()
    await state.update_data(message_gpt_id=msg.message_id)
    await state.set_state(WorkGPT.input_question)

async def stop_dialog(callback: CallbackQuery, state: FSMContext):
    await state.clear() 
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Выберете, что вы хотите от ИИ', 
        ),
        reply_markup=gpt_kb.gpt_main_kb
    )

async def stop_dialog_in_ai(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear() 
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await gm.bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=data['message_gpt_id'],
        media=InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Выберете, что вы хотите от ИИ', 
        ),
        reply_markup=gpt_kb.gpt_main_kb
    )
    await callback.message.delete()

async def to_main_from_ai(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await gm.bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=data['message_gpt_id'],
        media=InputMediaPhoto(
            media=gm.Media_tg.main_photo,
            caption=f"Добро пожаловать в {html.link('NewYear-Bot', 'https://t.me/new_artem_year_bot')}!\n"
                    f"Выберете, что вы хотите сделать в меню ниже ⬇️",
        ), 
        reply_markup=main_kb.main_menu_1(callback.from_user.id)
    )
    await callback.message.delete()

async def ai(message: Message, state: FSMContext):
    await state.set_state(WorkGPT.process)
    await state.update_data(process=message.text)
    data = await state.get_data()
    msg = await gm.bot.edit_message_media(
        chat_id=message.chat.id,
        message_id=data['message_gpt_id'],
        media=InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Ответ генерируется...'
        )
    )
    await message.delete()
    res = await generate_ai(data['process'])
    if res is not None:
        answer_q = res.choices[0].message.content
        try:
            await message.answer(
                text=answer_q,
                parse_mode='markdown',
                reply_markup=gpt_kb.next_kb
            )
            await msg.edit_media(
                InputMediaPhoto(
                    media=gm.Media_tg.gpt_photo,
                    caption=f'Ответ успешно сгенерирован на вопрос: `{data["process"]}`',
                    parse_mode='markdown'
                )
            )
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

#ANECDOTE
async def gen_more_anecdote(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await state.set_state(WorkGPT.process)
    msg = await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Анекдот генерируется...'
        )
    )
    res = await generate_anecdote()
    
    if res is not None:
        answer_q = res.choices[0].message.content
        try:
            await callback.message.edit_media(
                InputMediaPhoto(
                    media=gm.Media_tg.gpt_photo,
                    caption=answer_q,
                    parse_mode='markdown'
                ),
                reply_markup=gpt_kb.next_anecdote_kb
            )
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
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await state.set_state(WorkGPT.process)
    msg = await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Анекдот генерируется...'
        )
    )
    res = await generate_anecdote()
    
    if res is not None:
        answer_q = res.choices[0].message.content
        try:
            await callback.message.edit_media(
                InputMediaPhoto(
                    media=gm.Media_tg.gpt_photo,
                    caption=answer_q,
                    parse_mode='markdown'
                ),
                reply_markup=gpt_kb.next_anecdote_kb
            )
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
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.set_state(WorkGPT.message_gpt_id)
    msg = await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Выберете пол вашего друга'
        ),
        reply_markup=gpt_kb.gender_kb
    )
    await state.update_data(message_gpt_id=msg.message_id)
    

async def men_fr(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.update_data(gender='другу')
    await state.set_state(InfAboutFriend.age)
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Сколько лет вашему другу?'
        )
    )
    
async def women_fr(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.update_data(gender='подруге')
    await state.set_state(InfAboutFriend.age)
    await callback.message.edit_media(
        InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Сколько лет вашей подруге?'
        )
    )

async def age_fr(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        a = int(message.text)
        if a > 0:
            await state.update_data(age=message.text)
            await state.set_state(InfAboutFriend.hobby)
            if data["gender"] == 'другу':
                text = 'вашего друга'
            else:
                text = 'вашу подругу'
            await gm.bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=data['message_gpt_id'],
                media=InputMediaPhoto(
                    media=gm.Media_tg.gpt_photo,
                    caption=f'Опишите {text}, какой характер, хобби и т.д.'
                )
            )
            await message.delete()
        else:
            try:
                await gm.bot.edit_message_media(
                    chat_id=message.chat.id,
                    message_id=data['message_gpt_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.gpt_photo,
                        caption='Такого возраста не существует ❌'
                    )
                )
                await message.delete()
            except TelegramBadRequest:
                await message.delete()
    except ValueError:
        try:
            await gm.bot.edit_message_media(
                    chat_id=message.chat.id,
                    message_id=data['message_gpt_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.gpt_photo,
                        caption='Введите возраст цифрами 🔢'
                    )
                )
            await message.delete()
        except TelegramBadRequest:
            await message.delete()

async def hobby_fr(message: Message, state: FSMContext):
    await state.update_data(hobby=message.text)
    global DATA
    global TEXT
    DATA = await state.get_data()
    
    await state.set_state(WorkGPT.process)
    msg = await gm.bot.edit_message_media(
        chat_id=message.chat.id,
        message_id=DATA['message_gpt_id'],
        media=InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Cписок подарков генерируется...'
        )
    )
    await message.delete()
    res = await generate_presents(gender=DATA["gender"], age=DATA["age"], hobby=DATA["hobby"])
    
    if res is not None:
        if DATA["gender"] == 'другу':
            TEXT = f'Вашему {DATA["age"]}-летнему другу, который {DATA["hobby"]}, может понравится:\n\n'
        else:
            TEXT = f'Вашей {DATA["age"]}-летней подруге, которая {DATA["hobby"]}, может понравится:\n\n'
        answer_q = TEXT + res.choices[0].message.content
        try:
            await msg.edit_media(
                InputMediaPhoto(
                    media=gm.Media_tg.gpt_photo,
                    caption=answer_q,
                    parse_mode='markdown'
                ),
                reply_markup=gpt_kb.next_presents_kb
            )
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
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.set_state(WorkGPT.process)
    global DATA
    global TEXT
    msg = await gm.bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=DATA['message_gpt_id'],
        media=InputMediaPhoto(
            media=gm.Media_tg.gpt_photo,
            caption='Cписок подарков генерируется...'
        )
    )
    res = await generate_presents(gender=DATA["gender"], age=DATA["age"], hobby=DATA["hobby"])
    
    if res is not None:
        answer_q = TEXT + res.choices[0].message.content
        try:
            await msg.edit_media(
                InputMediaPhoto(
                    media=gm.Media_tg.gpt_photo,
                    caption=answer_q,
                    parse_mode='markdown'
                ),
                reply_markup=gpt_kb.next_presents_kb
            )
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
