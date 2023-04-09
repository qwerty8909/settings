import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

BASE_URL = 'https://www.cybersport.ru/?sort=-publishedAt'
HEADERS = {'User-Agent': UserAgent().random}


async def news_parser():
    links = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL, headers=HEADERS) as response:
                website_url = await aiohttp.StreamReader.read(response.content)
                soup = BeautifulSoup(website_url, 'lxml')

                news_link = soup.find_all('article')
                for news in news_link:
                    links.append(
                        {
                            'link': 'https://www.cybersport.ru' + news.find('a').get('href'),
                            'text': news.find('h3').get_text()
                        })
    except:
        pass

    return links


async def site_parser(link):
    news = ''
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=HEADERS) as response:
                website_url = await aiohttp.StreamReader.read(response.content)
                soup = BeautifulSoup(website_url, 'lxml')

                article_body = soup.find('article')
                # for p in article_body.find_all(["i", "em"]):
                #     p.extract()
                for td in article_body.find_all(['p']):
                    news += str(td.text).replace('\n', ' ') + '\n'

    except:
        pass

    return news


def site_parsera(link):
    return asyncio.run(site_parser(link))

# print(asyncio.run(news_parser()))
print(asyncio.run(site_parser('https://www.cybersport.ru/tags/cs-go/poluchal-priglashenie-ot-big-boleet-za-manchester-siti-znaet-dyrachyo-i-boitsia-jame-v-klatche-interviu-s-kair0n-iz-vp')))
# if __name__ == '__main__':
#     asyncio.run(news_parser())
