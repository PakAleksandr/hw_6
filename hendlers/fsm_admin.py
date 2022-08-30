from aiogram.dispatcher import  FSMContext
from aiogram import types, Dispatcher
from config import bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db

ID=None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    discription = State()
    price = State()

async def make_change_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'что надо хозяин')
    await message.delete()

async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply("фото")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Tеперь введи название")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply("Введи описание")


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['disription'] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь укажи цену")

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)

    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()

async def cancel_registration(message: types.Message, state: FSMContext):
    await message.answer("Заказ отменен")


    await sqlite_db.sql_add_command(state)
    await state.finish()


def register_handlers_fsmadmin(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state='*', commands='cancel')
    dp.register_message_handler(cancel_registration,
                                    Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin)
    dp.register_message_handler(load_description, state=FSMAdmin.discription)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_change_command, commands=['moderator'], is_chat_admin=True)