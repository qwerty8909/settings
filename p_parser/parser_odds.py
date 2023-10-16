import requests
from bs4 import BeautifulSoup
import datetime
import psycopg2
from settings import SETTINGS
import db_query

current_time = datetime.datetime.now()
GAMES = {'football': 'футбол', 'hockey': 'хоккей', 'basketball': 'баскетбол'}
DAYS = [current_time.date() + datetime.timedelta(days=i) for i in range(9)]


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
        soup = BeautifulSoup(response.content, 'lxml')
        soup = soup.find_all('div', class_='mdUFTlKDVVKGiLOEZObL')
        for match in soup:
            try:
                match_id = match.find_next(class_='vJTg9Y6aXBP4LGXUFeuQ').get('href').split('/')[-2]
                match_data = match.get_text('/').split('/')
                datetime_data = match_data[:2]
                datetime_str = f"{current_time.year}.{datetime_data[1]} {datetime_data[0]}"
                match_dt = datetime.datetime.strptime(datetime_str, "%Y.%d.%m %H:%M").timestamp()
                coms_data = match.find_next(class_='o3lSdElHvcllGoav29Vd jYgKuWcyqNdH_WMhoHJZ').get_text('/').split('/')
                match_com1, match_com2 = coms_data[0], coms_data[2]
                match_result = match.find_all(class_='p6CRVKu0JBIc0Re6wokg')
                match_values = [item.get_text() if item is not None else None for item in match_result]
                while len(match_values) < 3:
                    match_values.insert(1, None)
                result_list.append(
                    (match_id, match_dt, match_com1, match_com2, match_values[0], match_values[1], match_values[2])
                )
            except ValueError:
                continue

    return result_list


# Функция для вставки данных в базу данных
def data_to_base(cursor, url, game):
    result_list = parse_data(url)
    print(game, len(result_list))
    for value in result_list:
        match_id, dt, com1, com2, p1, x, p2 = value
        # Проверка, если время меньше текущего времени, то пропустить вставку
        if datetime.datetime.fromtimestamp(dt) < current_time:
            continue
        # Вставка значений в таблицу
        cursor.execute(db_query.insert_elements_games, (match_id, dt, game, com1, com2, p1, x, p2))


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
    cursor.execute(db_query.create_table_games)
    # Удаление строк, где значение в столбце 'dt' меньше текущей даты и времени
    cursor.execute(db_query.delete_elements_games, (current_time,))
    conn.commit()

    for key, value in GAMES.items():
        for day in DAYS:
            url = f'https://odds.ru/{key}/match/{day}/'
            data_to_base(cursor, url, value)
            conn.commit()
    # закрытие соединения
    conn.close()


if __name__ == "__main__":
    main()
