import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from main.db_select import select_account, update_id, select_address, select_indicator, update_indicator
from main.keyboard import keyboard_off, keyboard_on, keyboard_indicator

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
    account = State()
    indicator = State()


# приветствие
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("_Введите лицевой счет_", reply_markup=keyboard_off(), parse_mode="Markdown")
    await PromptState.account.set()
    log_bot(f"{message.chat.id} - new START command")


# привязка id к лицевому счету
@dp.message_handler(state=PromptState.account)
async def id_to_account(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        update_id(message.chat.id, message.text)
        await message.answer(
            f"_Ваш телефон привязан к следующему адресу:_ *{select_address(message.text)}*",
            reply_markup=keyboard_on(), parse_mode="Markdown")
        log_bot(f"{message.chat.id} - user get or change account and get address")

    except:
        await message.answer(f'_Такой лицевой счет не существует._', parse_mode="Markdown")
        await send_welcome(message)


# выбор кнопки 'Передача показаний счетчиков'
@dp.message_handler(lambda message: message.text == 'Передача показаний счетчиков')
async def counters_button(message: types.Message):
    log_bot(f"{message.chat.id} - button {message.text}")
    await message.answer("_Выберите счетчик_", reply_markup=keyboard_indicator(message.chat.id), parse_mode="Markdown")


# выбор кнопки 'Сменить адрес'
@dp.message_handler(lambda message: message.text == 'Сменить адрес')
async def change_button(message: types.Message):
    log_bot(f"{message.chat.id} - button {message.text}")
    await send_welcome(message)


# выбор кнопки '<< Назад >>'
@dp.message_handler(lambda message: message.text == '<< Назад >>')
async def back_button(message: types.Message):
    log_bot(f"{message.chat.id} - button {message.text}")
    await send_welcome(message)


# вывод информации о счетчиках
async def handle_indication_button(message: types.Message, state: FSMContext, prompt: State):
    indicator_name = message.text
    await state.update_data(name=indicator_name)
    counter_date = select_indicator(indicator_dict[indicator_name][0], message.chat.id)
    counter_date = datetime.datetime.strptime(counter_date, "%Y-%m-%d %H:%M:%S").date()
    last_indicator = select_indicator(indicator_dict[indicator_name][1], message.chat.id)
    new_indicator = select_indicator(indicator_dict[indicator_name][2], message.chat.id) or 0
    await message.answer(
        f"_Дата следующей поверки счетчика : {counter_date}\nПредыдущее показание : {last_indicator}\nТекущее показание : {new_indicator}\nВведите новое текущее показание!_",
        reply_markup=keyboard_indicator(message.chat.id), parse_mode="Markdown")
    await prompt.set()


# применение текущих показаний
async def handle_counter_check(message: types.Message, state: FSMContext):
    data = await state.get_data()
    indicator_name = data.get('name')
    await state.finish()
    try:
        if float(message.text) >= select_indicator(indicator_dict[indicator_name][1], message.chat.id):
            update_indicator(indicator_dict[indicator_name][2], message.text, message.chat.id)
            await message.answer(f"_Данные успешно переданы_", reply_markup=keyboard_indicator(message.chat.id),
                                 parse_mode="Markdown")
            log_bot(f"{message.chat.id} - button '{indicator_name}' send indicator")
        else:
            await message.answer(
                f"_Текущие оказания счетчика не могут быть меньше предыдущего. Возможно Вы ошиблись счетчиком. Заново выберите счетчик и введите показание!_",
                reply_markup=keyboard_indicator(message.chat.id), parse_mode="Markdown")
            log_bot(f"{message.chat.id} - button '{indicator_name}' error indicator. small number")
    except:
        await message.answer(
            f"_Можно вводить только цифры и символ '.' для ввода десятичных значений. Заново выберите счетчик и введите показание!_",
            reply_markup=keyboard_indicator(message.chat.id), parse_mode="Markdown")
        log_bot(f"{message.chat.id} - button '{indicator_name}' error indicator. entered not a number")


# выбор кнопки счетчика
@dp.message_handler(lambda message: message.text in indicator_dict.keys(), state='*')
async def indication_button_handler(message: types.Message, state: FSMContext):
    indicator = message.text
    await handle_indication_button(message, state, PromptState.indicator)
    log_bot(f"{message.chat.id} - button '{indicator}'")


# ввод текущих показаний
@dp.message_handler(state=PromptState, content_types=types.ContentTypes.TEXT)
async def counter_check_handler(message: types.Message, state: FSMContext):
    await handle_counter_check(message, state)


# @dp.message_handler(lambda message: message.text == 'ХВС 1')
# async def indication_button(message: types.Message):
#     log_bot(f"{message.chat.id} - button 'ХВС 1'")
#     cold_1_date = sqlite_request(f"SELECT cold_1_date FROM bagration  WHERE id = {message.chat.id}")[0][0]
#     cold_1_date = datetime.datetime.strptime(cold_1_date, "%Y-%m-%d %H:%M:%S").date()
#     cold_1_last = sqlite_request(f"SELECT cold_1_last FROM bagration  WHERE id = {message.chat.id}")[0][0]
#     await message.answer(f"_Дата следующей поверки счетчика : {cold_1_date}\nПредыдущее показание : {cold_1_last}_", reply_markup=keyboard_counter(), parse_mode="Markdown")
#     await PromptState.prompt_cold_1.set()
#
#
# @dp.message_handler(state=PromptState.prompt_cold_1)
# async def counter_check(message: types.Message, state: FSMContext):
#     await state.finish()
#     if float(message.text) >= sqlite_request(f"SELECT cold_1_last FROM bagration  WHERE id = {message.chat.id}")[0][0]:
#         sqlite_request(f"UPDATE bagration SET cold_1_now = {message.text} WHERE id = {message.chat.id}")
#         await message.answer(f"_Данные успешно переданы_", reply_markup=keyboard_counter(), parse_mode="Markdown")
#         log_bot(f"{message.chat.id} - button 'ХВС 1' send indicator")
#     else:
#         await message.answer(f"_Текущие оказания счетчика не могут быть меньше предыдущего. Возможно Вы ошиблись счетчиком. Заново выберите счетчик и введите показание_", reply_markup=keyboard_counter(), parse_mode="Markdown")
#         log_bot(f"{message.chat.id} - button 'ХВС 1' error indicator. try again")
#
#
# @dp.message_handler(lambda message: message.text == 'ГВС 1')
# async def indication_button(message: types.Message):
#     log_bot(f"{message.chat.id} - button 'ГВС 1'")
#     cold_1_date = sqlite_request(f"SELECT hot_1_date FROM bagration  WHERE id = {message.chat.id}")[0][0]
#     cold_1_last = sqlite_request(f"SELECT hot_1_last FROM bagration  WHERE id = {message.chat.id}")[0][0]
#     await message.answer(f"_Дата поверки счетчика : {cold_1_date}\nПредыдущее показание : {cold_1_last}_", reply_markup=keyboard_counter(), parse_mode="Markdown")
#     await PromptState.prompt_hot_1.set()
#
#
# @dp.message_handler(state=PromptState.prompt_hot_1)
# async def counter_check(message: types.Message, state: FSMContext):
#     await state.finish()
#     sqlite_request(f"UPDATE bagration SET hot_1_now = {message.text} WHERE id = {message.chat.id}")
#     await message.answer(f"_Данные успешно переданы_", reply_markup=keyboard_counter(), parse_mode="Markdown")
#     log_bot(f"{message.chat.id} - button 'ГВС 1' send indicator")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
