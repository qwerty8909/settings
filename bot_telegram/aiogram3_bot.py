from aiogram import Bot, Dispatcher, types
from app.handlers.basic import get_start
import asyncio
import logging
from dotenv import load_dotenv
import os

load_dotenv()


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    bot = Bot(os.getenv("TOKEN"), parse_mode="MarkdownV2")
    dp = Dispatcher(bot=bot)
    dp.register_message_handler(get_start)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
