import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor
import time

# Create a cache for storing data from links
link_data_cache = {}

def file_maker(link):
    # Check if data for this link is already in cache
    if link in link_data_cache:
        website_url = link_data_cache[link]
    else:
        session = requests.Session()
        website_url = session.get(link).text
        link_data_cache[link] = website_url

    soup = BeautifulSoup(website_url, 'lxml')
    match = soup.find_all('div', class_='rlRGoA7qYO3NXvmrc4tr')
    ratio = [[text for text in item.stripped_strings] for item in match]
    bookmaker = [{0: item.find('a', class_='vJTg9Y6aXBP4LGXUFeuQ', href=True)['href']} for item in match]

    df_bookmaker = pd.DataFrame(bookmaker)
    if df_bookmaker.shape[1] == 1:
        df_ratio = pd.DataFrame(ratio)
        df_result = pd.concat([df_bookmaker[0].str.split("/").str[5], df_ratio[[1, 2, 3]]], axis=1, keys=['bookmaker', 'p1', 'x', 'p2'])
        df_result.to_csv(filename + '.csv', index=False)

time_start = time.time()
type_game = ['football', 'hockey', 'basketball']

with ProcessPoolExecutor() as executor:
    for name_game in type_game:
        site_link = 'https://odds.ru/' + name_game
        session = requests.Session()
        site_url = session.get(site_link).text
        site_soup = BeautifulSoup(site_url, 'lxml')
        game_site = site_soup.find_all('div', class_='mdUFTlKDVVKGiLOEZObL a.vJTg9Y6aXBP4LGXUFeuQ')
        links = ['https://odds.ru' + item['href'] for item in game_site]

        for link in links:
            filename = name_game + '-' + link.split('/')[5]
            if session.get(link).status_code == 200:
                executor.submit(file_maker, link)
            else:
                continue

time_end = time.time()
print(time_end - time_start)
