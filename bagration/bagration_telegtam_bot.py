import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


bot = Bot(token='5857478137:AAHtaIcU4OR08Yzu_kAglh_Gvr6DHjmObGI')
dp = Dispatcher(bot)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard = keyboard.add(KeyboardButton('/reboot_device_1'))
keyboard = keyboard.add(KeyboardButton('/reboot_device_2'))


async def send_message_to_device(chat_id, device_token, message):
    device_bot = Bot(device_token)
    await device_bot.send_message(chat_id=chat_id, text=message)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    print(message)
    await message.answer("_Hello_", reply_markup=keyboard, parse_mode="Markdown")


@dp.message_handler(commands=['reboot_device_1'])
async def device_1_reboot_command(message: types.Message):
    chat_id = message.chat.id
    await send_message_to_device(chat_id, '5867008896:AAFLEaQrXs4nPnhpuKWD5AGNKUc0NZNQ2sI', 'start')
    await message.answer("_device 1 reboot_", reply_markup=keyboard, parse_mode="Markdown")


@dp.message_handler(commands=['reboot_device_2'])
async def device_2_reboot_command(message: types.Message):
    chat_id = message.chat.id
    await send_message_to_device(chat_id, '5867008896:AAFLEaQrXs4nPnhpuKWD5AGNKUc0NZNQ2sI', 'start')
    await message.answer("_device 2 reboot_", reply_markup=keyboard, parse_mode="Markdown")


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
