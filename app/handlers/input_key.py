import os
import json

from aiogram import F, html, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramNetworkError

from ..database.requests import check_ban_user
from ..keyboards import key_kb, main_kb
from ..states.states import SecretKey
from ..utils import get_media as gm

COMPLETED_FILE = "completed_users.txt"

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
            if message.from_user.id == int(USER_GIFT_LIST['MokArtiy']):
                await message.delete()
                await gm.bot.edit_message_media(
                    chat_id=message.chat.id, 
                    message_id=data['message_id'],
                    media=InputMediaPhoto(
                        media=gm.Media_tg.key_photo,
                        # caption='Подарочный ключ на новогоднее поздравление для Ангелины был успешно применён!\n'
                        #         'Чтобы забрать подарок, выберете действие ниже ⬇️',
                        caption='У вас 6 непрочитанных сообщений...'
                    ),
                    reply_markup=key_kb.read_from_key           
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
        

#ДЕНЬ РОЖДЕНИЯ 31.10.2025
async def create_celebrate(message: Message):
    try:
        await gm.bot.send_photo(
            chat_id="7606461322",
            photo="AgACAgIAAxkBAAIFNGkD_uCMIAOHtAg-GoMEAp6sFhCEAAI__jEbWmohSFmpe7h2WtEcAQADAgADeQADNgQ",
            caption="Люди, появившиеся на свет 31 октября, рождены под знаком Скорпиона. Они сильны, решительны и энергичны. Скорпионы редко показывают чувства, но переживают все глубоко.\n\n"
            "Эти люди не боятся трудностей, стремятся к совершенству и умеют видеть то, что скрыто от других. Их интуиция и умение понимать людей помогают добиваться успеха в любой сфере — от искусства до политики и науки.\n\n"
            "А ещё 31 октября - Всемирный День Лемура!!! Ииии кажется он сбежал...Помоги поймать лемура, не переживай, они хоть и быстрые, но дыхалка у них так себе )",
            reply_markup=key_kb.celebrate_lemur
        )
        await message.answer("Сообщение отправлено.")
        
    except TelegramBadRequest as e:
        # Ошибки связанные с неправильными параметрами запроса
        error_message = "Ошибка в параметрах запроса: "
        if "chat not found" in str(e):
            error_message += "чат не найден"
        elif "file_id is invalid" in str(e):
            error_message += "неверный ID медиафайла"
        else:
            error_message += str(e)
        await message.answer(error_message)
        
    except TelegramNetworkError as e:
        # Проблемы с сетью
        await message.answer(f"Проблемы с сетью: {str(e)}")
        
    except TelegramAPIError as e:
        # Другие ошибки Telegram API
        await message.answer(f"Ошибка Telegram API: {str(e)}")
        
    except Exception as e:
        # Любые другие непредвиденные ошибки
        await message.answer(f"Непредвиденная ошибка: {str(e)}")

def load_completed_users():
    if not os.path.exists(COMPLETED_FILE):
        return set()
    with open(COMPLETED_FILE, "r", encoding="utf-8") as f:
        return {int(line.strip()) for line in f if line.strip().isdigit()}

def save_completed_user(user_id: int):
    with open(COMPLETED_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user_id}\n")
    
async def handle_webapp_data(message: Message):
    print("📥 Получено WebApp-данные:", message.web_app_data.data)
    print("👤 user_id:", message.from_user.id)
    try:
        data = json.loads(message.web_app_data.data)
        print("📦 Распакованные данные:", data)
        if data.get("action") == "lemur_caught":
            user_id = message.from_user.id
            completed = load_completed_users()
            print("✅ Загружен список завершивших:", completed)

            if user_id not in completed:
                print("🆕 Новый пользователь! Сохраняю и отправляю видео...")
                save_completed_user(user_id)
                await message.answer_video_note(
                    video_note="DQACAgIAAxkBAAIFU2kEf_CFExfpIriuLw9iLZl3dG0CAAJKiAACWmopSH8BF4BKRuJoNgQ"
                )
            else:
                print("🔁 Пользователь уже играл.")
                await message.answer("Уверен ты уже профи в ловле лемуров! Рад, что тебе понравилась игруля ) 💘")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        
async def read_messages(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer_video_note(
        video_note='DQACAgIAAxkBAAIFfWkEmYE5AZITrorFISPgpvNXrigoAAKXhgACWmopSPazAhs3Ps3KNgQ',
        reply_markup=key_kb.four_msg
    )

async def four_msg(callback: CallbackQuery): #достаток
    await callback.answer('')
    await callback.message.answer_video_note(
        video_note='DQACAgIAAxkBAAIFf2kEodpxoapXbguiEorAc8jCqzrxAALMiwACWmopSBOcAUNplfH8NgQ',
        reply_markup=key_kb.free_msg
    )
    
async def free_msg(callback: CallbackQuery): #черные/белые полосы
    await callback.answer('')
    await callback.message.answer_video_note(
        video_note='DQACAgIAAxkBAAIFgWkEo0SuaDFvJjVcULryHTv3iFYqAALciwACWmopSFYR9U7sIRxVNgQ',
        reply_markup=key_kb.two_msg
    )
    
async def two_msg(callback: CallbackQuery): #никого не слушай
    await callback.answer('')
    await callback.message.answer_video_note(
        video_note='DQACAgIAAxkBAAIFg2kEpDdQHxdBPxxAOiH0zBZfFfxJAALpiwACWmopSAhagvF8XzAqNgQ',
        reply_markup=key_kb.one_msg
    )
    
async def one_msg(callback: CallbackQuery): #позитив
    await callback.answer('')
    await callback.message.answer_video_note(
        video_note='DQACAgIAAxkBAAIFhWkEpWpB9XuAT3qasSmXpPFXy16FAAICjAACWmopSGcSUTAe2So4NgQ',
        reply_markup=key_kb.final_code_msg
    )
    
async def final_msg(callback: CallbackQuery): #финалочка
    await callback.answer('')
    await callback.message.answer_video_note(
        video_note='DQACAgIAAxkBAAIFh2kEpqah2DnxinYGazeVhUL0mcN2AAImjAACWmopSLDOCAw06kYmNgQ',
        reply_markup=key_kb.final_msg
    )
    
async def input_final_code(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer(text="Введи код, у тебя одна попытка!")
    await state.set_state(SecretKey.input_final_key)
    
async def code_final(message: Message, state: FSMContext):
    if message.text == "31-A-10-N-25-G-4-E-u-L":
        await state.clear()
        await gm.bot.send_message(chat_id="5034740706", text="Код активирован!")
        await message.answer("Успех, код активирован! Теперь немного подожди 🥳")
        await message.answer_video_note(video_note="DQACAgIAAxkBAAIFlmkEwaHS7JlTjLR7NLLom77Y3x1rAALTjQACWmopSIl_YwEMFbAHNgQ")
    else:
        await message.answer("Ладно, подумай ещё и введи снова...")
        await gm.bot.send_message(chat_id="5034740706", text="Она ошиблась епта")

#НОВЫЙ ГОД 31.12.2025
RESULTS = {
    "true_music": "Готово ✅",
    "start_results": "Подвести итоги 🎄",
    "to_main_from_gift": "Влететь в 2026 🥂"
}

CARDS = [
    "AgACAgIAAxkBAAIGLWlU5nPUejazNgFWbp5VeOcGilmMAAJKC2sbEE-pSqigtowjp1hJAQADAgADeQADOAQ",
    "AgACAgIAAxkBAAIGO2lU6C6efoXzE4hjOTlWkIYF7t54AALpDGsbrjmoSmeFAmJfFDw0AQADAgADeQADOAQ",
    "AgACAgIAAxkBAAIGPWlU6ERs2F7itcPG1rmTJckRDCGhAAJXC2sbEE-pSvZcooMj1Dn5AQADAgADeQADOAQ",
    "AgACAgIAAxkBAAIGP2lU6F9WMO9bjnajhf7b62JtPhNuAAJaC2sbEE-pSqdEGnpGORqtAQADAgADeQADOAQ",
    "AgACAgIAAxkBAAIGQWlU6HETEy_c_7Oap3bmWsIqQB-GAAJcC2sbEE-pSq2UiWoF-Cu7AQADAgADeQADOAQ",
    "AgACAgIAAxkBAAIGQ2lU6IAPWj7cCWAkAAG9EkSm7HKoUQACXQtrGxBPqUoAAWAmlLIgeJcBAAMCAAN5AAM4BA",
    "AgACAgIAAxkBAAIGRWlU6I0tOICe7isdH0dDaV5mJ5dwAAJeC2sbEE-pSmGgHgjfc5mRAQADAgADeQADOAQ",
    "AgACAgIAAxkBAAIGR2lU6Jmdy-XsSHNncD-4fyRI101RAAJfC2sbEE-pStNdU1O7ZrQlAQADAgADeQADOAQ"
]

async def summarize_results(message: Message):
    try:
        await gm.bot.send_audio(
            chat_id=USER_GIFT_LIST['Artemiy'],
            audio="CQACAgIAAxkBAAIGI2lU5Ib_Z8flETGE4XmL3DmQrnbCAAIyhgACVfepSgMDPw-LcwABuTgE", #АУДИО
            caption="Настройся на правильный ритм 🎧",
            reply_markup=key_kb.generate_results_kb("true_music", RESULTS['true_music'])
        )
        await message.answer("Сообщение отправлено.")
        
    except TelegramBadRequest as e:
        # Ошибки связанные с неправильными параметрами запроса
        error_message = "Ошибка в параметрах запроса: "
        if "chat not found" in str(e):
            error_message += "чат не найден"
        elif "file_id is invalid" in str(e):
            error_message += "неверный ID медиафайла"
        else:
            error_message += str(e)
        await message.answer(error_message)
        
    except TelegramNetworkError as e:
        # Проблемы с сетью
        await message.answer(f"Проблемы с сетью: {str(e)}")
        
    except TelegramAPIError as e:
        # Другие ошибки Telegram API
        await message.answer(f"Ошибка Telegram API: {str(e)}")
        
    except Exception as e:
        # Любые другие непредвиденные ошибки
        await message.answer(f"Непредвиденная ошибка: {str(e)}")

async def joining_the_results(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_reply_markup(reply_markup=None)
    await gm.bot.send_photo(
                chat_id=USER_GIFT_LIST['Artemiy'],
                photo=CARDS[0],
                caption="Совсем немного осталось до конца года, поэтому я предлагаю вспомнить лучшие моменты и подвести небольшие итоги.",
                reply_markup=key_kb.get_photo_keyboard(current_index=0, total=len(CARDS))
            )
    await gm.bot.send_message(
        chat_id=USER_GIFT_LIST['Artemiy'], 
        text="Поводит итоги")
    
async def start_results(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=CARDS[1],
            caption="🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄"
        ),
        reply_markup=key_kb.get_photo_keyboard(current_index=1, total=len(CARDS))
    )
    
async def navigate_photos(callback: CallbackQuery):
    try:
        index = int(callback.data.split("_")[1])
    except (IndexError, ValueError):
        await callback.answer("Ошибка навигации.")
        return

    if index < 0 or index >= len(CARDS):
        await callback.answer("Недопустимая страница.")
        return

    if index == 0:
        caption = "Совсем немного осталось до конца года, поэтому я предлагаю вспомнить лучшие моменты и подвести небольшие итоги."
    else:
        caption = "🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄"
    
    card = CARDS[index]
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=card,
            caption=caption),
        reply_markup=key_kb.get_photo_keyboard(current_index=index, total=len(CARDS))
    )
    await callback.answer('')
    
async def was_cool(callback: CallbackQuery):
    await callback.answer('')
    media = [
        InputMediaPhoto(media=file_id)
        for file_id in CARDS
    ]
    await callback.message.answer_media_group(media=media)
    await callback.message.answer_video_note(
        video_note="DQACAgIAAxkBAAIFlmkEwaHS7JlTjLR7NLLom77Y3x1rAALTjQACWmopSIl_YwEMFbAHNgQ", #КРУЖОК
        reply_markup=key_kb.generate_results_kb(key="to_main_from_gift", value=RESULTS['to_main_from_gift'])
    )