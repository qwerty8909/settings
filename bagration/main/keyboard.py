from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .db_select import select_button


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
    keyboard = ReplyKeyboardRemove()
    return keyboard


def keyboard_on():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = keyboard.add(KeyboardButton('Передача показаний счетчиков'))
    keyboard = keyboard.add(KeyboardButton('Сменить адрес'))
    keyboard = keyboard.add(KeyboardButton('Оставить заявку в АДС'))
    return keyboard


def keyboard_indicator(tg_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_row = [
        KeyboardButton(dict_button_first[key_button])
        for key_button in dict_button_first.keys()
        if select_button(key_button, tg_id)[0][0]
    ]
    keyboard.row(*button_row)
    button_row = [
        KeyboardButton(dict_button_second[key_button])
        for key_button in dict_button_second.keys()
        if select_button(key_button, tg_id)[0][0]
    ]
    keyboard.row(*button_row).row(KeyboardButton('<< Назад >>'))
    return keyboard