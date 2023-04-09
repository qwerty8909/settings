# загружаем необходимые модули и библиотеки
import requests
import datetime as dt
import pandas as pd
import psycopg2
import psycopg2.extras as extras
from bs4 import BeautifulSoup

time_start = dt.datetime.now()


# функция для переноса датафрейма в базу SQL
def execute_values(conn, df, table):
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cur = conn.cursor()
    try:
        extras.execute_values(cur, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
        return 1
    cur.close()


# подключаемся к серверу
conn = psycopg2.connect(database="betting",
                        host="88.218.169.217",
                        port="5432",
                        user="postgres",
                        password="ZXC12VBN")
conn.autocommit = False
cursor = conn.cursor()

# готовим ссылки для каждого спортивного события и датафрейм с событиями на сегодня и завтра
games = ['football', 'hockey', 'basketball']
days = [dt.date.today(), dt.date.today() + dt.timedelta(days=1)]
links = []
book = []
bookmakers = []

for game in games:
    for day in days:
        game_link = 'https://odds.ru/' + game + '/match/' + day.strftime('%Y-%m-%d')
        game_url = requests.get(game_link).text
        game_soup = BeautifulSoup(game_url, 'lxml')
        game_match = game_soup.find_all('div', class_='mdUFTlKDVVKGiLOEZObL')
        for site in game_match:
            links.append(site.find('div').find_next(class_='vJTg9Y6aXBP4LGXUFeuQ').get('href'))
            book.append(
                {
                    'id': site.find('div').find_next(class_='vJTg9Y6aXBP4LGXUFeuQ').get('href').split("/")[3],
                    'com1': site.find('div').find_next(class_='o3lSdElHvcllGoav29Vd jYgKuWcyqNdH_WMhoHJZ').get_text(
                        '/').split("/")[0],
                    'com2': site.find('div').find_next(class_='o3lSdElHvcllGoav29Vd jYgKuWcyqNdH_WMhoHJZ').get_text(
                        '/').split("/")[2],
                    'game': game,
                    'dt': dt.datetime.combine(day, dt.datetime.strptime([text for text in site.stripped_strings][0],
                                                                        "%H:%M").time())
                })
df_games = pd.DataFrame(book)
# Создаем файл с результатом работы программы
# df_games.to_csv('df_games-' + dt.date.today().strftime('%Y-%m-%d') + '.csv', index=False, encoding='utf-8')

# у каждого события собираем букмекеров с коэффициентами и создаем еще один датафрейм
for link in links:
    link_link = 'https://odds.ru' + link
    link_url = requests.get(link_link).text
    link_soup = BeautifulSoup(link_url, 'lxml')
    link_match = link_soup.find_all('div', class_='rlRGoA7qYO3NXvmrc4tr')
    if len(link_match) > 0:
        for item in link_match:
            bookmakers.append(
                {
                    'id': link.split("/")[3],
                    'bookmaker': item.find('div').find_next(target='_blank').get('href').split("/")[5],
                    'p1': ([text for text in item.stripped_strings])[1],
                    'x': ([text for text in item.stripped_strings])[2],
                    'p2': ([text for text in item.stripped_strings])[3]
                })
    else:
        continue
df_bookmaker = pd.DataFrame(bookmakers)

# Создаем файл с результатом работы программы
# df_bookmaker.to_csv('df_bookmaker-' + dt.date.today().strftime('%Y-%m-%d') + '.csv', index=False, encoding='utf-8')

# очищаем базы, заполняем новыми данными, и отключаемся от сервера
truncate_games = '''TRUNCATE public.games, public.bookmaker;'''
cursor.execute(truncate_games)
execute_values(conn, df_games, 'public.games')
execute_values(conn, df_bookmaker, 'public.bookmaker')
conn.commit()
cursor.close()
conn.close()

# считаем время работы скрипта
time_end = dt.datetime.now()
print('Время работы скрипта: ', time_end - time_start)
