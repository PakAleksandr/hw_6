from aiogram import types, Dispatcher
from config import bot
from config import ADMIN
import random



async def game_1(message: types.Message):

    if message.text.startswith("play") and message.from_user.id in ADMIN:
        lst = ['⚽️', '🏀', '🎰', '🎳' '🎯']
        a = random.choice(lst)
        await bot.send_dice(message.chat.id, emoji=a)


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(game_1)