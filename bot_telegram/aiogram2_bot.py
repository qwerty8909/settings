import aiogram.types
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import BotCommandScopeDefault
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - [%(levelname)s] - %(name)s - '
                           '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
load_dotenv()
bot = Bot(os.getenv("TOKEN"), parse_mode="MarkdownV2")
dp = Dispatcher(bot=bot)


async def set_commands():
    await bot.set_my_commands([
        types.BotCommand(command='/start', description='Начало работы'),
        types.BotCommand(command='/help', description='Помощь'),
        types.BotCommand(command='/cancel', description='Сбросить'),
    ])


async def start_bot(_):
    await set_commands()
    await bot.send_message(os.getenv("ADMIN_ID"), text='Бот запущен')
    logging.info('Bot started')


async def stop_bot(_):
    await bot.send_message(os.getenv("ADMIN_ID"), text='Бот остановлен')
    logging.info('Bot stopped')


@dp.message_handler(commands=['start'])
async def get_start(message: types.Message):
    await bot.send_message(message.from_user.id, f'~Привет, {message.from_user.first_name}~')
    await message.answer(f'_Привет, {message.from_user.first_name}, второй раз_')
    await message.reply(f'__Привет, {message.from_user.first_name}, третий раз__')
    logging.info(f'Button "{message.text}"')


@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def get_photo(message: types.Message):
    await message.answer(f'Ты отправил картинку')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'photo.jpg')
    logging.info('Get picture')


@dp.message_handler(text=['Привет'])
async def get_hello(message: types.Message):
    await message.answer(f'И тебе привет')
    logging.info(f'Text: "{message.text}"')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=start_bot, on_shutdown=stop_bot, skip_updates=True)
