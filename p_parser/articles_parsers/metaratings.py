import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime
import re

HEADERS = {'User-Agent': UserAgent().random}


async def as_news_parser():
    links = []
    games = ['futbol', 'hokkey', 'basketbol', 'tennis', 'voleybol']
    try:
        async with aiohttp.ClientSession() as session:
            for game in games:
                link = f'https://metaratings.ru/prognozy/{game}/'
                async with session.get(link, headers=HEADERS) as response:
                    website_url = await aiohttp.StreamReader.read(response.content)
                    soup = BeautifulSoup(website_url, 'lxml')

                    soup = soup.find('div', class_='forecast-tabWrap').find_next('div', class_='')
                    for p in soup.find_all("a", target="_blank")[-5:]:
                        if p.find("span"):
                            p.extract()
                    news_link = soup.find_all('a')
                    for news in news_link:
                        url_link = 'https://metaratings.ru' + news.get('href')
                        news_time = news.find_next('div').find_next('div').find_next('div').get_text()
                        news_time_match = re.match(re.compile(r'\d{2}:\d{2}:\d{2}'), news_time)
                        news_text_match = re.match(r'Прогноз на матч (\w.+) [–—] (\w.+)[.:]', news.get_text())
                        if news_time_match and news_text_match:
                            current_time = datetime.datetime.now()
                            hours, minutes, seconds = map(int, news_time.split(':'))
                            target_time = current_time + datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

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

                article_body = soup.find("article", class_=None)
                for p in article_body.find_all("p")[-3:]:
                    if p.find("b"):
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