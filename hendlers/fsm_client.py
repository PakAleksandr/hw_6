from aiogram import types, Dispatcher
from config import bot
from keyboard import client_kb
from data_base import sqlite_db

async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=client_kb)
        await message.delete()
    except:
        await message.reply( 'Общение с ботом только через ЛС, напишите ему https://web.telegram.org/z/#5485253044')

async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Вс-Чт с 10:00 до 23:00")


async def pizza_place_command(message: types.Message):
    await bot.send_message (message.from_user.id,  'ул. московская 1/3')


async def pizza_menu_command(message: types.message):
   await sqlite_db.sql_read(message)




def register_handlers_fsmclient(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим работы'])
    dp.register_message_handler(pizza_place_command, commands=['Располажение'])
    dp.register_message_handler(pizza_menu_command,commands=['Меню'])
