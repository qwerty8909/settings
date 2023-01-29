# загружаем необходимые модули и библиотеки
import requests
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras as extras

# подключаемся к серверу
conn = psycopg2.connect(database = "postgres",
                        host = "localhost",
                        user = "postgres",
                        password = "1234",
                        port = "5432")
conn.autocommit = False
cursor = conn.cursor()

# готовим фрейм для ссылок по каждому спортивному событию сегодня и завтра
games = ['football', 'hockey', 'basketball']
days = [dt.date.today(), dt.date.today() + dt.timedelta(days=1)]
book = []
for game in games:
    for day in days:
        link = 'https://odds.ru/' + game + '/match/' + day.strftime('%Y-%m-%d')
        url = requests.get(link).text
        soup = BeautifulSoup(url, 'lxml')
        match = soup.find_all('div', class_='mdUFTlKDVVKGiLOEZObL')
        for item in match:
            book.append(
                {
                    'id': item.find('div').find_next(class_='vJTg9Y6aXBP4LGXUFeuQ').get('href').split("/")[3],
                    'com1': item.find('div').find_next(class_='o3lSdElHvcllGoav29Vd jYgKuWcyqNdH_WMhoHJZ').get_text(
                        '/').split("/")[0],
                    'com2': item.find('div').find_next(class_='o3lSdElHvcllGoav29Vd jYgKuWcyqNdH_WMhoHJZ').get_text(
                        '/').split("/")[2],
                    'game': game,
                    'dt': dt.datetime.combine(day, dt.datetime.strptime([text for text in item.stripped_strings][0],
                                                                        "%H:%M").time())
                })

df_games = pd.DataFrame(book)
# Создаем файл с результатом работы программы
df_games.to_csv(dt.date.today().strftime('%Y-%m-%d') + '.csv', index=False, encoding='utf-8')  # encoding='cp1251'

# сохраняем в базу на сервере
def execute_values(conn, df, table):
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()

truncate_games = '''TRUNCATE public.games;'''
cursor.execute(truncate_games)
execute_values(conn, df_games, 'public.games')

# отключаемся
conn.commit()
cursor.close()
conn.close()