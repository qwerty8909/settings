from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .db_select import select_indicator_button, select_account_button


dict_button_first = {
    'cold_1_date': 'ХВС 1',
    'hot_1_date': 'ГВС 1',
    'cold_2_date': 'ХВС 2',
    'hot_2_date': 'ГВС 2',
}
dict_button_second = {
    'heat_date': 'Отопление',
    'power_date': 'Электроэнергия',
}


def keyboard_off():
    return ReplyKeyboardRemove()


def keyboard_on():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = keyboard.add(KeyboardButton('Получить ключ'))
    keyboard = keyboard.add(KeyboardButton('Оплатить VPN'))
    return keyboard

def keyboard_back():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = keyboard.add(KeyboardButton('< Назад >'))
    return keyboard


def keyboard_indicator(account):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_row = [
        KeyboardButton(dict_button_first[key_button])
        for key_button in dict_button_first.keys()
        if select_indicator_button(key_button, account)[0][0]
    ]
    keyboard.row(*button_row)
    button_row = [
        KeyboardButton(dict_button_second[key_button])
        for key_button in dict_button_second.keys()
        if select_indicator_button(key_button, account)[0][0]
    ]
    keyboard.row(*button_row).row(KeyboardButton('< Назад >'))
    return keyboard


def keyboard_address(tg_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_row = [
        KeyboardButton(button)
        for button in [item[0] for item in select_account_button(tg_id)]
    ]
    keyboard.row(*button_row).row(KeyboardButton('Добавить ЛС'), KeyboardButton('< Главное меню >'))
    return keyboard