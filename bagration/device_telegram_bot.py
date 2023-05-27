import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance
bot = Bot(token='5867008896:AAFLEaQrXs4nPnhpuKWD5AGNKUc0NZNQ2sI')

# Create a dispatcher instance
dp = Dispatcher(bot)


# Define a handler for incoming messages
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.text == 'start':
        await message.answer("_Hello my friend!_", parse_mode="Markdown")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
