import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="5857478137:AAHtaIcU4OR08Yzu_kAglh_Gvr6DHjmObGI")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Define states
class UserState(StatesGroup):
    WaitingForName = State()


# Start command handler
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Enter your name!")
    await UserState.WaitingForName.set()


# Restart command handler
@dp.message_handler(commands=['restart'])
async def cmd_restart(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    await message.reply(f"{name}, do you want to change your name? Enter your name!")
    await UserState.WaitingForName.set()


# Text message handler
@dp.message_handler(state=UserState.WaitingForName)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.reply(f"Hi {name}!")
    await state.finish()


if __name__ == '__main__':
    # Start the bot
    executor.start_polling(dp, skip_updates=True)
