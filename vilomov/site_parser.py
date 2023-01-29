# загружаем необходимые модули и библиотеки
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup


def file_maker():
    website_url = requests.get(link).text
    soup = BeautifulSoup(website_url, 'lxml')
    match = soup.find_all('div', class_='rlRGoA7qYO3NXvmrc4tr')
    ratio = []
    bookmaker = []

    # если есть датафрейм с букмекерами
    for item in match:
        bookmaker.append({0: item.find('div').find_next(target='_blank').get('href')})
    df_bookmaker = pd.DataFrame(bookmaker)
    if df_bookmaker.shape[1] == 1:
        # то создаем датафрейм с коэффициентами
        for item in match:
            ratio.append([text for text in item.stripped_strings])
        df_ratio = pd.DataFrame(ratio)

        # создаем результирующий датафрейм
        df_result = pd.concat([df_bookmaker[0].str.split("/").str[5], df_ratio[[1, 2, 3]]], axis=1, join='inner')
        df_result.columns = ['bookmaker', 'p1', 'x', 'p2']
        # Создаем файл с результатом работы программы
        df_result.to_csv(filename + '.csv')


# готовим фрейм для ссылок по каждому спортивному событию
time_start = datetime.datetime.now()
type_game = ['football', 'hockey', 'basketball']
for name_game in type_game:
    site_link = 'https://odds.ru/' + name_game
    site_url = requests.get(site_link).text
    site_soup = BeautifulSoup(site_url, 'lxml')
    site_match = site_soup.find_all('div', class_='mdUFTlKDVVKGiLOEZObL')
    game_site = []
    for item in site_match:
        game_site.append({0: item.find('div').find_next(class_='vJTg9Y6aXBP4LGXUFeuQ').get('href')})

    for row in game_site:
        link = 'https://odds.ru' + row[0]
        filename = name_game + '-' + link.split('/')[5]
        # проверяем доступность сайта (увеличивает время работы скрипта в 2 раза)
        if requests.get(link).status_code == 200:
            file_maker()
        else:
            continue

time_end = datetime.datetime.now()
print('Время работы скрипта: ', time_end - time_start)
