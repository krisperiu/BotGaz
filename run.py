import aiogram
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers import router
from database.models import async_main


async def main():
    load_dotenv()
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')