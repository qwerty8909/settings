import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from main.db_select import check_user_account, insert_user_account, check_account, select_account_address, \
    select_address, select_indicator, update_indicator, del_account
from main.keyboard import keyboard_back, keyboard_on, keyboard_indicator, keyboard_address

telegram_token = "5857478137:AAHtaIcU4OR08Yzu_kAglh_Gvr6DHjmObGI"

bot = Bot(telegram_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

indicator_dict = {
    'ХВС 1': ("cold_1_date", "cold_1_last", "cold_1_now"),
    'ГВС 1': ("hot_1_date", "hot_1_last", "hot_1_now"),
    'ХВС 2': ("cold_2_date", "cold_2_last", "cold_2_now"),
    'ГВС 2': ("hot_2_date", "hot_2_last", "hot_2_now"),
    'Отопление': ("heat_date", "heat_last", "heat_now"),
    'Электроэнергия': ("power_date", "power_last", "power_now"),
}


def log_bot(log_text):
    now = datetime.datetime.now().replace(microsecond=0)
    log = f'{now} - {log_text}'
    print(log)


class PromptState(StatesGroup):
    address = State()
    account = State()
    counter = State()


# приветствие
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    log_bot(f"{message.chat.id} - button 'START'")
    await message.answer(f"_Здравствуйте!\nВыберите действие!_", reply_markup=keyboard_on(), parse_mode="Markdown")


# выбор кнопки '< Главное меню >'
@dp.message_handler(lambda message: message.text == '< Главное меню >', state='*')
async def menu_button(message: types.Message, state: FSMContext):
    log_bot(f"{message.chat.id} - button '{message.text}'")
    await message.answer(f"_В главное меню_", reply_markup=keyboard_on(), parse_mode="Markdown")
    await state.finish()


# выбор кнопки '< Назад >'
@dp.message_handler(lambda message: message.text == '< Назад >', state='*')
async def back_button(message: types.Message):
    await counters_button(message)


# выбор кнопки 'Передача показаний счетчиков'
@dp.message_handler(lambda message: message.text == 'Передать показания счетчиков', state='*')
async def counters_button(message: types.Message):
    log_bot(f"{message.chat.id} - button '{message.text}'")
    if len(keyboard_address(message.chat.id).keyboard[0]):
        await message.answer("_Выберите квартиру_", reply_markup=keyboard_address(message.chat.id),
                             parse_mode="Markdown")
        await PromptState.address.set()
    else:
        await message.answer("_Добавьте квартиру_", reply_markup=keyboard_address(message.chat.id),
                             parse_mode="Markdown")


# сопоставить адрес и id
@dp.message_handler(lambda message: message.text == 'Добавить ЛС', state='*')
async def add_account(message: types.Message):
    log_bot(f"{message.chat.id} - button '{message.text}'")
    await message.answer("_Введите лицевой счет квартиры!_", reply_markup=keyboard_back(), parse_mode="Markdown")
    await PromptState.account.set()


# привязка id к лицевому счету
@dp.message_handler(state=PromptState.account)
async def id_to_account(message: types.Message, state: FSMContext):
    account_id = message.text
    await state.finish()
    try:
        if check_user_account(message.chat.id, account_id):
            log_bot(f"{message.chat.id} - user set to account - ok, exist")
            await message.answer(f"_Ваш телефон уже привязан к адресу:_ *{select_address(account_id)}*",
                                 reply_markup=keyboard_address(message.chat.id), parse_mode="Markdown")
            await counters_button(message)
        elif check_account(account_id):
            log_bot(f"{message.chat.id} - user set to account - ok, new")
            insert_user_account(message.chat.id, account_id)
            await message.answer(f"_Ваш телефон привязан к следующему адресу:_ *{select_address(account_id)}*",
                                 reply_markup=keyboard_address(message.chat.id), parse_mode="Markdown")
            await counters_button(message)
        else:
            log_bot(f"{message.chat.id} - user set to account - error, not exist")
            await message.answer(f'_Такой лицевой счет не существует. Повторите ввод!_', parse_mode="Markdown")
            await PromptState.account.set()
    except:
        log_bot(f"{message.chat.id} - user set to account - error, not number")
        await message.answer(f'_Лицевой счет состоит только из цифр. Повторите ввод!_', parse_mode="Markdown")
        await PromptState.account.set()


@dp.message_handler(state=PromptState.address)
async def select_apartment_id(message: types.Message, state: FSMContext):
    try:
        account_id = message.text
        await message.answer(f"_Адрес: {select_account_address(account_id)}\nВыберите счетчик_",
                             reply_markup=keyboard_indicator(account_id), parse_mode="Markdown")
        await state.update_data(account_id=account_id)
        log_bot(f"{message.chat.id} - button '{message.text}'")
        await PromptState.counter.set()
    except:
        await PromptState.address.set()


# выбор кнопки счетчика
@dp.message_handler(lambda message: message.text in indicator_dict.keys(), state=PromptState.counter)
async def indication_button_handler(message: types.Message, state: FSMContext):
    counter = message.text
    await state.update_data(counter=counter)
    data = await state.get_data()
    account_id = data.get('account_id')
    counter_date = select_indicator(indicator_dict[counter][0], account_id)
    counter_date = datetime.datetime.strptime(counter_date, "%Y-%m-%d %H:%M:%S").date()
    last_indicator = select_indicator(indicator_dict[counter][1], account_id)
    new_indicator = select_indicator(indicator_dict[counter][2], account_id) or 0
    log_bot(f"{message.chat.id} - button '{message.text}'")
    if counter_date > datetime.datetime.now().date():
        await message.answer(
            f"_Дата следующей поверки счетчика : {counter_date}\nПредыдущее показание : {last_indicator}\nТекущее "
            f"показание : {new_indicator}\nВведите новое текущее показание!_",
            reply_markup=keyboard_indicator(account_id), parse_mode="Markdown")
        await PromptState.counter.set()
    else:
        await message.answer(
            f"_У данного счетчика истек межповерочный интервал. Показания не принимаются! Выберите другой счетчик!_",
            reply_markup=keyboard_indicator(account_id), parse_mode="Markdown")
        await PromptState.counter.set()


# ввод текущих показаний
@dp.message_handler(state=PromptState, content_types=types.ContentTypes.TEXT)
async def counter_check_handler(message: types.Message, state: FSMContext):
    indicator = message.text
    data = await state.get_data()
    account_id = data.get('account_id')
    counter = data.get('counter')
    try:
        indicator_float = float(indicator.replace(",", "."))
        if indicator_float >= select_indicator(indicator_dict[counter][1], account_id):
            log_bot(f"{message.chat.id} - button '{counter}' - ok, good indicator")
            update_indicator(indicator_dict[counter][2], indicator_float, account_id)
            await message.answer(f"_Данные успешно переданы_", reply_markup=keyboard_indicator(account_id),
                                 parse_mode="Markdown")
        else:
            log_bot(f"{message.chat.id} - button '{counter}' - error, small indicator")
            await message.answer(
                f"_Текущие показания счетчика не могут быть меньше предыдущего. Возможно Вы ошиблись счетчиком. "
                f"Заново выберите счетчик и введите показание!_",
                reply_markup=keyboard_indicator(account_id), parse_mode="Markdown")
    except:
        if counter:
            log_bot(f"{message.chat.id} - button '{counter}' - error, not number")
            await message.answer(f"_Некорректное значение.\nЗаново выберите счетчик и введите показание!_",
                                 reply_markup=keyboard_indicator(account_id), parse_mode="Markdown")
        else:
            log_bot(f"{message.chat.id} - button '{counter}' - error, button None")
            await message.answer(f"_Сперва выберите счетчик!_", reply_markup=keyboard_indicator(account_id),
                                 parse_mode="Markdown")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
