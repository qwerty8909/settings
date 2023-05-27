import openai
import requests
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from deep_translator import GoogleTranslator
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# prod
# openai.api_key = "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"
# telegram_token = "5445332563:AAFLddxllZ2YdDrnIM0eO8hjeLhmYneKveM"
# path = r'/home/project/chat_log.txt'
# test
openai.api_key = "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"
telegram_token = "5857478137:AAHtaIcU4OR08Yzu_kAglh_Gvr6DHjmObGI"
path = r'C:\Users\vitalii\IdeaProjects\settings\server\chat_log.txt'




bot = Bot(telegram_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard = keyboard.add(KeyboardButton('Очистить историю!'))
keyboard = keyboard.add(KeyboardButton('Нарисовать картинку!'))
chat = {}


class PromptState(StatesGroup):
    prompt = State()


def write_chat(log_text):
    now = datetime.datetime.now().replace(microsecond=0)
    log = f'{now} - {log_text}'
    print(log)
    with open(path, 'a') as file:
        file.write(log + "\n")


def update(messages, role, content):
    messages.append({'role': role, 'content': GoogleTranslator(source='ru', target='en').translate(content)})
    return messages


def chat_gpt(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    result = response.choices[0].message['content']
    return result


def stable_diffusion(prompt):
    prompt = GoogleTranslator(source='ru', target='en').translate(prompt)
    url = "https://stablediffusionapi.com/api/v3/text2img"
    payload = {"key": "4lTHuAaagxTcTbWcMg9gdl4yFus4RvoShLSvFkl9Qr7yjLrAzFI2nZViYQ0E",
               "prompt": prompt,
               "negative_prompt": None,
               "enhance_prompt": "no",
               "width": "512",
               "height": "512",
               "samples": "1",
               "num_inference_steps": "30",
               "guidance_scale": 7.5,
               "seed": None,
               }
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)
    picture = ''.join(eval(response.text.replace('null', '"null"'))['output']).replace('\\', '')

    return picture


# users = {328854598, 2054855742}
# accepted_users = lambda message: message.from_user.id not in users
# @dp.message_handler(accepted_users, content_types=['any'])
# async def handle_unwanted_users(message: types.Message):
#     await message.answer("Извините, бот работает только для одобренных пользователей.")
#     return


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.chat.id
    if user_id not in chat.keys():
        chat[user_id] = []
        log_text = f'{str(user_id)} - new user_id added to database!'
        write_chat(log_text)
    else:
        log_text = f'{str(user_id)} - user_id is already in database!'
        write_chat(log_text)
    await message.answer("_Добро пожаловать!_", reply_markup=keyboard, parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == 'Очистить историю!')
async def process_clear_command(message: types.Message):
    user_id = message.chat.id
    chat[user_id] = []
    log_text = f'{str(user_id)} - clear chat_history user_id!'
    write_chat(log_text)
    await message.answer("*ВНИМАНИЕ!* \n_История общения очищена!_", reply_markup=keyboard, parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == 'Нарисовать картинку!')
async def process_generation_command(message: types.Message):
    await message.answer('_Введите описание картинки_', parse_mode="Markdown")
    await PromptState.prompt.set()


@dp.message_handler(state=PromptState.prompt)
async def process_prompt(message: types.Message, state: FSMContext):
    prompt = message.text
    await state.finish()
    user_id = message.chat.id
    log_text = f'{str(user_id)} - picture "{prompt}"'
    write_chat(log_text)
    await message.answer(stable_diffusion(prompt), reply_markup=keyboard, parse_mode="Markdown")


@dp.message_handler()
async def send(message: types.Message):
    user_id = message.chat.id
    try:
        messages = chat.get(user_id)
        update(messages, 'user', message.text)
        result = chat_gpt(messages)
        await message.answer(GoogleTranslator(source='en', target='ru').translate(result))
        update(messages, 'assistant', result)
        chat[user_id] = messages
        log_text = f'{str(user_id)} - chat_history contains {len(chat[user_id]) / 2} lines'
        write_chat(log_text)
    except openai.error.InvalidRequestError:
        await message.answer('*ОШИБКА!* \n_История общения очищена! \nВы использовали все токены или не ввели '
                             'текст! \nМожете продолжать пользоваться ботом, но он забыл все о чем вы '
                             'переписывались!_', parse_mode="Markdown")
        chat[user_id] = []
        log_text = f'{str(user_id)} - InvalidRequestError! clear chat_history user_id!'
        write_chat(log_text)
    except openai.error.RateLimitError:
        await message.answer('*ОШИБКА!* \n_Чат временно не работает!_', parse_mode="Markdown")
        chat[user_id] = []
        log_text = f'{str(user_id)} - RateLimitError! clear chat_history user_id!'
        write_chat(log_text)
    except AttributeError:
        await message.answer('*ОШИБКА СЕРВЕРА!* \n_Повторите запрос!_', parse_mode="Markdown")
        chat[user_id] = []
        log_text = f'{str(user_id)} - AttributeError! clear chat_history user_id!'
        write_chat(log_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
