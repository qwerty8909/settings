import requests
from bs4 import BeautifulSoup
import datetime
import psycopg2
from settings import SETTINGS
import db_query
import json

current_time = datetime.datetime.now()
BASE_URL = 'https://prognozist.ru/engine/ajax/match_center.php?action=showMatchCenterPage&sport_id=582&match_date='
DAYS = [current_time.date() + datetime.timedelta(days=i) for i in range(4)]

# Функция для выполнения HTTP-запроса с обработкой ошибок
def make_request(url):
    try:
        response = requests.get(url)
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
        data = json.loads(response.text)
        soup = BeautifulSoup(data['content'], 'html.parser')
        for tr in soup.select('tr.match-row'):
            tips = ''
            link = 'https://prognozist.ru' + tr.select_one('a.match-row__event')['href']
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            coms = soup.find_all('div', class_='match-info__team-name')
            com1 = coms[0].get_text().lstrip()
            com2 = coms[1].get_text().lstrip()
            dt = soup.find('time').get('datetime')
            timestamp = datetime.datetime.fromisoformat(dt).timestamp()
            items = soup.find_all('div', class_='mc-block-tip__item')
            for item in items:
                a = item.find('div', class_='mc-block-tip__odd')
                b = item.find('div', class_='mc-block-tip__tip')
                c = item.find('div', class_='mc-block-tip-item__description')
                a = a.get_text().strip() if a else ''
                b = b.get_text().strip() if b else ''
                c = c.get_text().strip() if c else ''
                if a == 'Купить':
                    continue
                tip_text = f'Прогноз: {a} - {b}'
                if c:
                    tip_text += f' - {c}'
                tips += f'{tip_text} '

            len_tips = sum(len(i) for i in tips)
            print(f'{len_tips} - {link}')
            result_list.append((link, com1, com2, timestamp, tips))

    return result_list


# Функция для вставки данных в базу данных
def data_to_base(cursor, url, current_time):
    result_list = parse_data(url)
    for value in result_list:
        link, com1, com2, dt, tips = value
        # Проверка, если время меньше текущего времени, то пропустить вставку
        if datetime.datetime.fromtimestamp(dt) < current_time:
            continue
        # Вставка значений в таблицу
        cursor.execute(db_query.insert_elements_prognozist, (link, com1, com2, dt, tips))


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
    cursor.execute(db_query.create_table_prognozist)
    # Удаление строк, где значение в столбце 'dt' меньше текущей даты и времени
    cursor.execute(db_query.delete_elements_prognozist, (current_time,))
    conn.commit()

    for day in DAYS:
        url = BASE_URL + f'{day.strftime("%Y-%m-%d")}&mc_page_type=tips'
        data_to_base(cursor, url, current_time)
        conn.commit()
    # закрытие соединения
    conn.close()


if __name__ == "__main__":
    main()
