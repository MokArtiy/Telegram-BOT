import os

from aiogram import F, html, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from ..database.requests import check_ban_user
from ..keyboards import key_kb, main_kb
from ..states.states import SecretKey
from ..utils import get_media as gm


USER_GIFT_LIST = {
    'Angelina' : '6522122306',
    'Valeria' : '1925153198',
    'Marina' : '972959754',
    'Artemiy' : '5034740706',
    'MokArtiy' : '7606461322'
}
GIFT_KEYS = {
    'Angelina' : '26-G-12-E-24-L-4-I-u-A',
    'Valeria' : 'L-26-E-12-R-24-A',
    'Marina' : 'C-26-H-12-E-24-E-4-S-u-E',
    'Artemiy' : '123',
    'MokArtiy' : '123'
}


async def return_to_key(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await state.clear()
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
            caption='Ого! Да вы везунчик!\nВыберете действие в меню ниже ⬇️',
            media=gm.Media_tg.key_photo
        ),
        reply_markup=key_kb.key_main_kb
    )
    
async def return_to_key_from_gift(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await callback.message.edit_reply_markup(None)
    await callback.message.answer_photo(
        caption='Ого! Да вы везунчик!\nВыберете действие в меню ниже ⬇️',
        photo=gm.Media_tg.key_photo,
        reply_markup=key_kb.key_main_kb
    )

async def to_main_from_gift(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await callback.message.edit_reply_markup(None)
    await callback.message.answer_photo(
        photo=gm.Media_tg.main_photo,
        caption=f"Добро пожаловать в {html.link('NewYear-Bot', 'https://t.me/new_artem_year_bot')}!\n"
                f"Выберете, что вы хотите сделать в меню ниже ⬇️",
        reply_markup=main_kb.main_menu_1(callback.from_user.id)
    )

async def secret_key_main(callback: CallbackQuery):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await callback.message.edit_media(
        InputMediaPhoto(
        media=gm.Media_tg.key_photo,
        caption='Ого! Да вы везунчик!\nВыберете действие в меню ниже ⬇️',
        ),
        reply_markup=key_kb.key_main_kb
    )
    
async def input_key(callback: CallbackQuery, state: FSMContext):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    await callback.answer('')
    await state.set_state(SecretKey.message_id)
    msg = await callback.message.edit_media(
        InputMediaPhoto(
            caption='Введите свой подарочный код!',
            media=gm.Media_tg.key_photo,
        ),
        reply_markup=key_kb.return_key_kb
    )
    await state.update_data(message_id=msg.message_id)
    await state.set_state(SecretKey.input_key)
    
async def check_key(message: Message, state: FSMContext):
    
    if (await check_ban_user(message.from_user.id)):
        return await message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    global USER_GIFT_LIST, GIFT_KEYS
    data = await state.get_data()
    if message.text in GIFT_KEYS.values():
        if message.text == GIFT_KEYS['Angelina']:
            if message.from_user.id == int(USER_GIFT_LIST['Angelina']):
                await message.delete()
                await gm.bot.edit_message_media(
                    chat_id=message.chat.id, 
                    message_id=data['message_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.key_photo,
                        caption='Подарочный ключ на новогоднее поздравление для Ангелины был успешно применён!\n'
                                'Чтобы забрать подарок, выберете действие ниже ⬇️',
                    ),
                    reply_markup=key_kb.get_gift           
                )
                await state.clear()
            else:
                await message.delete()
                await gm.bot.edit_message_media(
                    chat_id=message.chat.id, 
                    message_id=data['message_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.key_photo,
                        caption='К сожалению, это не ваш ключ... Верните его владельцу!',
                    ),
                    reply_markup=key_kb.return_key_kb
                )
        if message.text == GIFT_KEYS['Marina']:
            if message.from_user.id == int(USER_GIFT_LIST['Marina']):
                await message.delete()
                await gm.bot.edit_message_media(
                    chat_id=message.chat.id, 
                    message_id=data['message_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.key_photo,
                        caption='Подарочный ключ на новогоднее поздравление для Марины был успешно применён!\n'
                                'Чтобы забрать подарок, выберете действие ниже ⬇️',
                    ),
                    reply_markup=key_kb.get_gift           
                )
                await state.clear()
            else:
                await message.delete()
                await gm.bot.edit_message_media(
                    chat_id=message.chat.id, 
                    message_id=data['message_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.key_photo,
                        caption='К сожалению, это не ваш ключ... Верните его владельцу!',
                    ),
                    reply_markup=key_kb.return_key_kb
                )
        if message.text == GIFT_KEYS['Artemiy']:
            if message.from_user.id == int(USER_GIFT_LIST['Artemiy']):
                await message.delete()
                await gm.bot.edit_message_media(
                    chat_id=message.chat.id, 
                    message_id=data['message_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.key_photo,
                        caption='Подарочный ключ на новогоднее поздравление для Артемия был успешно применён!\n'
                                'Чтобы забрать подарок, выберете действие ниже ⬇️',
                    ),
                    reply_markup=key_kb.get_gift           
                )
            else:
                await message.delete()
                await gm.bot.edit_message_media(
                    chat_id=message.chat.id, 
                    message_id=data['message_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.key_photo,
                        caption='Ты реально думаешь, что сможешь его подобрать? Не страдай хуйней, займись делом.',
                    ),
                    reply_markup=key_kb.return_key_kb
                )
                await state.clear()
        if message.text == GIFT_KEYS['Valeria']:
            if message.from_user.id == int(USER_GIFT_LIST['Valeria']):
                await message.delete()
                await gm.bot.edit_message_media(
                    chat_id=message.chat.id, 
                    message_id=data['message_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.key_photo,
                        caption='Подарочный ключ на подарок для Леры был успешно применён!\n'
                                'Чтобы забрать его, выберете действие ниже ⬇️',
                    ),
                    reply_markup=key_kb.get_gift           
                )
                await state.clear()
            else:
                await message.delete()
                await gm.bot.edit_message_media(
                    chat_id=message.chat.id, 
                    message_id=data['message_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.key_photo,
                        caption='К сожалению, это не ваш ключ... Верните его владельцу!',
                    ),
                    reply_markup=key_kb.return_key_kb
                )
    else:
        await message.delete()
        await gm.bot.edit_message_media(
            chat_id=message.chat.id,
            message_id=data['message_id'],
            media=InputMediaPhoto(
                media=gm.Media_tg.key_photo,
                caption='Код введён неверно ❌ Попробуйте снова...',
            ),
            reply_markup=key_kb.return_key_kb
        )
        
async def get_gift(callback: CallbackQuery):
    if (await check_ban_user(callback.from_user.id)):
        await callback.answer('')
        return await callback.message.answer(
            text=f'Вы забанены в данном боте, если вы не согласны с баном, свяжитесь с '
                 f'[Администратором](tg://user?id={5034740706}).',
            parse_mode='markdown')
    
    global USER_GIFT_LIST
    if callback.from_user.id == int(USER_GIFT_LIST['Artemiy']):
        await callback.answer('')
        await callback.message.delete()
        await callback.message.answer_video_note(
            FSInputFile(path='video/for_test.mp4'),
            reply_markup=key_kb.return_from_gift_key_kb
        )
    if callback.from_user.id == int(USER_GIFT_LIST['Angelina']):
        await callback.answer('')
        await callback.message.delete()
        await callback.message.answer_video_note(
            FSInputFile(path='video/for_angelina.mp4'),
            reply_markup=key_kb.return_from_gift_key_kb
        )
    if callback.from_user.id == int(USER_GIFT_LIST['Marina']):
        await callback.answer('')
        await callback.message.delete()
        await callback.message.answer_video_note(
            FSInputFile(path='video/for_marina.mp4'),
            reply_markup=key_kb.return_from_gift_key_kb
        )
    if callback.from_user.id == int(USER_GIFT_LIST['Valeria']):
        await callback.answer('')
        await callback.message.delete()
        await callback.message.answer_video_note(
            FSInputFile(path='video/for_valeria.mp4'),
            reply_markup=key_kb.return_from_gift_key_kb
        )