import requests
import urllib.parse
from bs4 import BeautifulSoup


def req_begin(link):
    sa_key = '6d11ce9f8a9a4cbcb977fb37a6518173'
    sa_api = 'https://api.scrapingant.com/v2/general'
    qParams = {'url': link, 'x-api-key': sa_key}
    req = f'{sa_api}?{urllib.parse.urlencode(qParams)}'
    response = requests.get(req)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def news_parser():
    links = []
    days = ['today/', 'tomorrow/']
    try:
        for day in days:
            soup = req_begin('https://bookmaker-ratings.ru/tips/' + day)
            news_link = soup.find_all('div', class_='sc-1b3f0cfb-6 hHDOXP')
            for news in news_link:
                links.append(
                    {
                        'link': 'https://bookmaker-ratings.ru' + news.find_next('a',
                                                                                class_='sc-8eaa09cb-1 dOUFle sc-1b3f0cfb-24 hVpmMm').get(
                            'href'),
                        'text': news.find('p').get_text()
                    })
    except:
        pass

    return links


def site_parser(link):
    news = ''
    try:
        soup = req_begin(link)
        article_body = soup.find("div", class_="sc-1c701fe1-5 jksxlO")
        for td in article_body.find_all('p', class_=None):
            news += str(td.text).replace('\n', '') + '\n'
    except:
        pass

    return news
