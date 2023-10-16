import requests
from bs4 import BeautifulSoup
import re
import datetime
import psycopg2
from settings import SETTINGS
import db_query

# Переменные с URL и заголовками
HEADERS = {'X-Fsign': 'SW9D1eZo'}
BASE_URL = 'https://local-ruua.flashscore.ninja/46/x/feed/'
# Паттерны для поиска данных
GAME_PATTERN = r'AA÷(\w+).*?AD÷(\d+).*?AE÷([\w\'/() -.]+).*?AF÷([\w\'/() -.]+)'
ODDS_PATTERN = r'AA÷(\w+)(?:.*?XA÷([\d.]+))?(?:.*?XB÷([\d.]+))?(?:.*?XC÷([\d.]+))?'
# переменные для выборки
GAMES = {'1': 'футбол', '2': 'теннис', '3': 'баскетбол', '4': 'хоккей', '12': 'волейбол'}
DAYS = range(8)


# Функция для выполнения HTTP-запроса с обработкой ошибок
def make_request(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


# Функция для парсинга данных с использованием регулярных выражений
def parse_data(url, pattern):
    result_dict = {}
    response = make_request(url)
    if response:
        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        data = soup.find('p')
        matches = re.finditer(pattern, str(data))
        for match in matches:
            key = match.group(1)
            values = [match.group(i) if match.group(i) is not None else None for i in range(2, 5)]
            result_dict[key] = values
    return result_dict


# Функция для вставки данных в базу данных
def data_to_base(cursor, game_url, odds_url, game, current_time):
    game_dict = parse_data(game_url, GAME_PATTERN)
    odds_dict = parse_data(odds_url, ODDS_PATTERN)
    print(game, len(game_dict))
    for key, values in game_dict.items():
        dt = int(values[0])
        com1 = values[1]
        com2 = values[2]
        # Проверка, если время меньше текущего времени, то пропустить вставку
        if datetime.datetime.fromtimestamp(dt) < current_time:
            continue
        odds_data = odds_dict.get(key, (None, None, None))
        # Вставка значений в таблицу
        cursor.execute(db_query.insert_elements_games,
                       (key, dt, game, com1, com2, odds_data[0], odds_data[1], odds_data[2]))


# Основная функция для выполнения запросов и обработки данных
def main():
    current_time = datetime.datetime.now()
    conn = psycopg2.connect(database=SETTINGS.db.database,
                            host=SETTINGS.db.host,
                            port=SETTINGS.db.port,
                            user=SETTINGS.db.user,
                            password=SETTINGS.db.password)
    conn.autocommit = False
    cursor = conn.cursor()
    # Создание таблицы, если она еще не существует
    cursor.execute(db_query.create_table_games)
    # Удаление строк, где значение в столбце 'dt' меньше текущей даты и времени
    cursor.execute(db_query.delete_elements_games, (current_time,))
    conn.commit()

    for key, value in GAMES.items():
        for day in DAYS:
            game_url = BASE_URL + f'f_{key}_{str(day)}_3_ru-kz_1'
            odds_url = BASE_URL + f'fo_{key}_{str(day)}_3_ru-kz_1_0'
            data_to_base(cursor, game_url, odds_url, value, current_time)
            conn.commit()
    # закрытие соединения
    conn.close()


if __name__ == "__main__":
    main()
