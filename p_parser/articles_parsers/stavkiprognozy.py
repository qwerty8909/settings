import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime

HEADERS = {'User-Agent': UserAgent().random}
current_time = datetime.datetime.now()


async def as_news_parser():
    links = []
    games = ['football', 'hockey', 'basketball', 'tennis']
    try:
        async with aiohttp.ClientSession() as session:
            for game in games:
                link = f'https://stavkiprognozy.ru/prognozy/{game}/'
                async with session.get(link, headers=HEADERS) as response:
                    website_url = await aiohttp.StreamReader.read(response.content)
                    soup = BeautifulSoup(website_url, 'html.parser')

                    news_link = soup.find_all('div', {'class': 'box-item-body announce-item-body'})
                    for news in news_link:
                        url_link = 'https://stavkiprognozy.ru' + news.find_next('a').get('href'),
                        news_text = news.find_next('div', class_='single-announce-team-title').get_text().split(' - ')
                        news_time = news.find_next('div', class_='single-announce-time').get_text().strip()
                        target_time = datetime.datetime.strptime(news_time, '%d.%m.%Y %H:%M')
                        if target_time < current_time:
                            continue

                        links.append((
                            url_link[0],
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

                article_body = soup.find("div", itemtype="http://schema.org/SportsEvent")
                for td in article_body.find_all('p', class_=None):
                    news += str(td.text).replace('\n', '') + '\n'
    except:
        pass

    return news


def news_parser():
    return asyncio.run(as_news_parser())


def site_parser(link):
    return asyncio.run(as_site_parser(link))