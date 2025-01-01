import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

class Media_tg:
    main_photo = FSInputFile('image/main.png')
    key_photo = FSInputFile('image/present.png')
    profile_photo = FSInputFile('image/profile.png')
    support_photo = FSInputFile('image/support.png')
    tools_photo = FSInputFile('image/tools.png')
    gpt_photo = FSInputFile('image/gpt.png')
    avatar_photo = FSInputFile('image/avatar.png')