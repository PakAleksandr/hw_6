import aioschedule
import asyncio
from aiogram import types, Dispatcher
from config import bot



async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await bot.send_message(chat_id=chat_id, text="Ok")

async def day_off():
    await bot.send_message(chat_id=chat_id, text="Хорошего отдыха!")


async def shcheduler():
    aioschedule.every().saturday.at("9:00").do(day_off)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)

def register_hendler_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id,
                                 lambda word: 'напомни' in word.text)