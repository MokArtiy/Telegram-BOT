from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.username)
    await message.answer('Добро пожаловать в маказин кроссовок!', reply_markup=await kb.main_menu())
    
    
@router.callback_query(F.data == 'to_main')
async def to_main(callback: CallbackQuery):
    await callback.answer('Вы вернулись в главное меню')
    await callback.message.edit_text('Добро пожаловать в маказин кроссовок!', reply_markup=await kb.main_menu())
    

@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('Вы перешли в каталог магазина')
    await callback.message.edit_text('Выберете категорию товара', reply_markup=await kb.categories())
    

@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.edit_text('Выберете товар по категории', 
                                  reply_markup=await kb.items(callback.data.split('_')[1]))
    
    
@router.callback_query(F.data.startswith('item_'))
async def item(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.edit_text(f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}$',
                                     reply_markup=await kb.buying_items())
    
    
@router.callback_query(F.data == 'add_to_basket')
async def add_to_basket(callback: CallbackQuery):
    await callback.answer('Хуй те, а не корзина, это заглушка', show_alert=True)