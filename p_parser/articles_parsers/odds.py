import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime
import re

HEADERS = {'User-Agent': UserAgent().random}

current_time = datetime.datetime.now()


async def as_news_parser():
    links = []
    games = ['football', 'hockey', 'basketball']
    try:
        async with aiohttp.ClientSession() as session:
            for game in games:
                link = f'https://odds.ru/{game}/forecasts/'
                async with session.get(link, headers=HEADERS) as response:
                    website_url = await aiohttp.StreamReader.read(response.content)
                    soup = BeautifulSoup(website_url, 'lxml')

                    news_link = soup.find_all('div', {'class': 'forecasts-post'})
                    for news in news_link:
                        news_time = news.find_next('time').get('datetime')
                        target_time = datetime.datetime.strptime(news_time, '%Y-%m-%d %H:%M')
                        if target_time < current_time:
                            continue
                        url_link = 'https://odds.ru' + news.find_next('div', {'class': 'forecasts-post__title'}).find_next('a').get('href')
                        news_text = news.find_next('div', {'class': 'forecasts-post__title'}).find_next('a').get_text()
                        news_text_match = re.search(r'«(\w.+)» [—–-] «(\w.+)»', news_text)
                        if news_text_match:

                            links.append((
                                url_link,
                                news_text_match.group(1),
                                news_text_match.group(2),
                                target_time.timestamp()
                            ))
    except:
        pass

    return links


async def as_site_parser(link):
    news = ''
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=HEADERS) as response:
                website_url = await aiohttp.StreamReader.read(response.content)
                soup = BeautifulSoup(website_url, 'lxml')

                article_body = soup.find('div', {'class': 'forecast-text'})
                for p in article_body.find_all("b")[-3:]:
                    if p.find("a"):
                        p.extract()
                for td in article_body.find_all('p', class_=None):
                    news += str(td.text).replace('\n', '') + '\n'
    except:
        pass

    return news


def news_parser():
    return asyncio.run(as_news_parser())


def site_parser(link):
    return asyncio.run(as_site_parser(link))
