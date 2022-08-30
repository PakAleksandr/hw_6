from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot
from keyboard.client_kb import cancel_markup, gender_markup


class FSMAdmin(StatesGroup):  # Finite State Machine
    photo_dish = State()
    dish_name = State()
    description = State()
    Meal_price = State()



async def photo_dish(message: types.Message, )






