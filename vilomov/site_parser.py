# загружаем необходимые модули и библиотеки
import requests
import pandas as pd
from bs4 import BeautifulSoup

def file_maker():
    website_url = requests.get(link).text
    soup = BeautifulSoup(website_url, 'lxml')
    match = soup.find_all('div', class_='rlRGoA7qYO3NXvmrc4tr')
    ratio = []
    bookmaker = []

    # датафреймы с коэффициентами и сайтом букмекера
    for item in match:
        ratio.append([text for text in item.stripped_strings])
    df_ratio = pd. DataFrame(ratio)

    for item in match:
        bookmaker.append({0 : item.find('div').find_next(target = '_blank').get('href')})
    df_bookmaker = pd. DataFrame(bookmaker)

    # создаем результирующий датафрейм
    df_result = pd.concat([df_bookmaker[0].str.split("/").str[5], df_ratio[[1,2,3]]], axis=1, join='inner')
    df_result.columns =['bookmaker', 'p1', 'x', 'p2']
    # Создаем файл с результатом работы программы
    df_result.to_csv(filename+'.csv')

link = 'https://odds.ru/football/match/borussia-dortmund-vs-1-fsv-mainz-05/251-481/'
filename = link.split('/')[5]
#проверяем доступность сайта
if requests.get(link).status_code == 200:
    file_maker()