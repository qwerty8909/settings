from aiogram import types


async def get_start(message: types.Message):
    await message.answer(f'_Привет, {message.from_user.first_name}, второй раз_')
    await message.reply(f'__Привет, {message.from_user.first_name}, третий раз__')

