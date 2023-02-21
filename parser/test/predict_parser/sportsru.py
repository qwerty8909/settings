from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def req_begin(link):
    req = Request(
        url=link,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    website_url = urlopen(req).read()
    soup = BeautifulSoup(website_url, 'lxml')
    return soup


def news_parser():
    links = []
    try:
        soup = req_begin('https://www.sports.ru/news/')
        news_link = soup.find_all('a', class_='short-text')
        for news in news_link[:100]:
            links.append(
                {
                    'link': 'https://www.sports.ru' + news.get('href'),
                    'text': news.get_text()
                })
    except:
        pass

    return links


def site_parser(link):
    news = ''
    try:
        soup = req_begin(link)
        article_body = soup.find("article")
        for td in article_body.find_all('p', class_=None)[:-2]:
            news += str(td.text).replace('\n', '') + '\n'
    except:
        pass

    return news
