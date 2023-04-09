import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from deep_translator import GoogleTranslator

telegram_token = "5445332563:AAFLddxllZ2YdDrnIM0eO8hjeLhmYneKveM"
openai.api_key = "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"
chat = {}

bot = Bot(telegram_token)
dp = Dispatcher(bot)


def update(messages, role, content):
    messages.append({'role': role, 'content': GoogleTranslator(source='ru', target='en').translate(content)})
    return messages


# users = {328854598, 2054855742}
# accepted_users = lambda message: message.from_user.id not in users
# @dp.message_handler(accepted_users, content_types=['any'])
# async def handle_unwanted_users(message: types.Message):
#     await message.answer("Извините, бот работает только для одобренных пользователей.")
#     return

@dp.message_handler()
async def send(message: types.Message):
    user_id = message.chat.id
    if user_id not in chat.keys():
        chat[user_id] = []
        print('new chat user_id - ', user_id)

    if message.text == '/start':
        chat[user_id] = []
        print('clear chat user_id - ', user_id)

    else:
        try:
            messages = chat.get(user_id)
            update(messages, 'user', message.text)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                # max_tokens=4000,
            )
            result = response.choices[0].message['content']
            await message.answer(GoogleTranslator(source='en', target='ru').translate(result))
            update(messages, 'assistant', result)
            chat[user_id] = messages
            print(user_id, ' - ', chat[user_id])
        except openai.error.InvalidRequestError:
            await message.answer('ОШИБКА! История общения очищена! \nВы использовали все токены или не ввели текст! '
                                 '\nМожете продолжать пользоваться ботом, но он забыл все о чем вы переписывались!')
            chat[user_id] = []
            print('Error! clear chat user_id - ', user_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
