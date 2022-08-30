from aiogram.utils import executor
from config import dp
from hendlers import notification
import logging
import asyncio

async def on_startup():
    asyncio.create_task(notification.shcheduler())
notification.register_hendler_notification(dp)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)