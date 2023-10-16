import urllib3
import datetime
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from outline_vpn.outline_vpn import OutlineVPN

telegram_token = "5857478137:AAHtaIcU4OR08Yzu_kAglh_Gvr6DHjmObGI"
client = OutlineVPN(api_url="https://88.218.169.217:59540/jBvNVZn-pm2c4MNzTG99Kg")

urllib3.disable_warnings()

bot = Bot(telegram_token)
dp = Dispatcher(bot)


def log_bot(log_text):
    now = datetime.datetime.now().replace(microsecond=0)
    log = f'{now} - {log_text}'
    print(log)


def set_limit():
    today = datetime.date.today()
    first_day_next_month = datetime.date(today.year, today.month + 1, 1)
    date_str = first_day_next_month.strftime('%Y-%m-%d')
    return date_str


def sqlite_request(request, params=()):
    with sqlite3.connect(r"C:\Users\vitalii\IdeaProjects\settings\test.db") as con:
        cur = con.cursor()
        cur.execute(request, params)
        result = cur.fetchall()
        con.commit()
    return result


def check_account(account):
    result = sqlite_request("SELECT count(account) FROM outline_tg WHERE account = (?);", (account,))
    return result[0][0]


def insert_data(account, payment):
    sqlite_request("INSERT INTO outline_tg (account, payment) VALUES (?, ?);", (account, payment))


def select_date(account):
    result = sqlite_request("SELECT payment FROM outline_tg WHERE account = (?);", (account,))
    return result[0][0]


def keyboard_on():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = keyboard.add(KeyboardButton('Get Key'))
    keyboard = keyboard.add(KeyboardButton('Pay VPN'))
    return keyboard


def keyboard_payment():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = keyboard.add(KeyboardButton('1 month'))
    keyboard = keyboard.add(KeyboardButton('2 month'))
    keyboard = keyboard.add(KeyboardButton('3 month'))
    keyboard = keyboard.add(KeyboardButton('Back'))
    return keyboard


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    log_bot(f"{message.chat.id} - button 'START'")
    await message.answer(f"_Hello!_", reply_markup=keyboard_on(), parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == 'Get Key')
async def get_key(message: types.Message):
    log_bot(f"{message.chat.id} - button '{message.text}'")
    if check_account(message.chat.id):
        log_bot(f"{message.chat.id} - old key")
        old_key = next((key.access_url for key in client.get_keys() if key.name == str(message.chat.id)), '')
        await message.answer(f"_You have the key already:_", reply_markup=keyboard_on(), parse_mode="Markdown")
        await message.answer(f"*{old_key}*", reply_markup=keyboard_on(), parse_mode="Markdown")
    else:
        log_bot(f"{message.chat.id} - new key")
        new_key = client.create_key(key_name=message.chat.id)
        insert_data(message.chat.id, set_limit())
        await message.answer(f"_Here is your new key:_", reply_markup=keyboard_on(), parse_mode="Markdown")
        await message.answer(f"*{new_key.access_url}*", reply_markup=keyboard_on(), parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == 'Pay VPN')
async def pay_vpn(message: types.Message):
    log_bot(f"{message.chat.id} - button '{message.text}'")
    await message.answer(f"_your date '{select_date(message.chat.id)}'_", reply_markup=keyboard_payment(), parse_mode="Markdown")


@dp.message_handler(lambda message: message.text in ['1 month', '2 month', '3 month'])
async def payment_months_handler(message: types.Message):
    log_bot(f"{message.chat.id} - button '{message.text}'")
    months = int(message.text.split()[0])
################################################
    await message.answer(f"Payment for {months} months is ok!")


@dp.message_handler(lambda message: message.text == 'Back')
async def back_handler(message: types.Message):
    log_bot(f"{message.chat.id} - button '{message.text}'")
    await message.answer(f"_Hello! Hello! Hello!_", reply_markup=keyboard_on(), parse_mode="Markdown")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
