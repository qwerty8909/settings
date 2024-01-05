import requests
from bs4 import BeautifulSoup
import datetime
import psycopg2
from deep_translator import GoogleTranslator
from settings import SETTINGS
import db_query
import json
from fake_useragent import UserAgent

current_time = datetime.datetime.now()
BASE_URL = 'https://betwatch.fr/football/getMoney?live_only=false&prematch_only=true&settings_order=score&utc=3&step=20'
HEADERS = {'User-Agent': UserAgent().random}


# Функция для выполнения HTTP-запроса с обработкой ошибок
def make_request(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


# Функция для парсинга данных
def parse_data(url):
    result_list = []
    response = make_request(url)
    if response:
        soup = BeautifulSoup(response.content, 'lxml')
        json_data = soup.p.get_text()
        data = json.loads(json_data)
        # Извлечение данных
        for item in data['data']:
            if item['n'] == 'Match Odds':
                match_id = item['e']
                date_time  = item['ce']
                dt = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ').timestamp()
                com1 = GoogleTranslator(source='en', target='ru').translate(item['i'][0][0])
                com2 = GoogleTranslator(source='en', target='ru').translate(item['i'][2][0])
                total = item['i'][0][1] + item['i'][1][1] + item['i'][2][1]
                p1 = item['i'][0][1] / total * 100 if item['i'][0][1] else 0
                x = item['i'][1][1] / total * 100 if item['i'][1][1] else 0
                p2 = item['i'][2][1] / total * 100 if item['i'][2][1] else 0
                result_list.append(
                    (match_id, dt + 3 * 3600, com1, com2, p1, x, p2)
                )
    return result_list


# Функция для вставки данных в базу данных
def data_to_base(cursor, url):
    result_list = parse_data(url)
    print(len(result_list))
    for value in result_list:
        match_id, dt, com1, com2, p1, x, p2 = value
        # Проверка, если время меньше текущего времени, то пропустить вставку
        if datetime.datetime.fromtimestamp(dt) < current_time:
            continue
        # Вставка значений в таблицу
        cursor.execute(db_query.insert_elements_betwatch, (match_id, dt, com1, com2, p1, x, p2))


# Основная функция для выполнения запросов и обработки данных
def main():
    conn = psycopg2.connect(database=SETTINGS.db.database,
                            host=SETTINGS.db.host,
                            port=SETTINGS.db.port,
                            user=SETTINGS.db.user,
                            password=SETTINGS.db.password)
    conn.autocommit = False
    cursor = conn.cursor()
    # Создание таблицы, если она еще не существует
    cursor.execute(db_query.create_table_betwatch)
    # Удаление строк, где значение в столбце 'dt' меньше текущей даты и времени
    cursor.execute(db_query.delete_elements_betwatch, (current_time,))
    conn.commit()

    data_to_base(cursor, BASE_URL)
    conn.commit()
    # закрытие соединения
    conn.close()


if __name__ == "__main__":
    main()
