import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime

BASE_URL = 'https://www.liveresult.ru/tips'
HEADERS = {'User-Agent': UserAgent().random}

today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1)


async def as_news_parser():
    links = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL, headers=HEADERS) as response:
                website_url = await aiohttp.StreamReader.read(response.content)
                soup = BeautifulSoup(website_url, 'lxml')

                soup = soup.find('div', {'class': 'tips-list'})
                news_link = soup.find_all('div', {'class': 'tips-list-tip'})
                for news in news_link:
                    url_link = 'https://www.liveresult.ru' + news.find('a').get('href')
                    news_text = news.find('a').get_text().strip().split('\n')
                    news_time = news.find('time').get_text()
                    if 'Сегодня в' in news_time:
                        # Если время сегодня, то заменяем "Сегодня" на текущую дату
                        news_time = news_time.replace('Сегодня в', today.strftime('%d.%m.%Y'))
                    elif 'Завтра в' in news_time:
                        # Если время завтра, то заменяем "Завтра" на завтрашнюю дату
                        news_time = news_time.replace('Завтра в', tomorrow.strftime('%d.%m.%Y'))
                    target_time = datetime.datetime.strptime(news_time, '%d.%m.%Y %H:%M')

                    links.append((
                        url_link,
                        news_text[0],
                        news_text[1],
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

                article_body = soup.find('div', {'class': 'tip-page-tex article-text mb-3'})
                for td in article_body.find_all('p', class_=None):
                    news += str(td.text).replace('\xa0', '').replace('\n', '') + '\n'
    except:
        pass

    return news


def news_parser():
    return asyncio.run(as_news_parser())


def site_parser(link):
    return asyncio.run(as_site_parser(link))