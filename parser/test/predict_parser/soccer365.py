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
        soup = req_begin('https://soccer365.ru/news/')
        news_link = soup.find_all('div', class_='articles_title')
        for news in news_link:
            links.append(
                {
                    'link': news.find('a').get('href'),
                    'text': news.find('a').get_text()
                })
    except:
        pass

    return links


def site_parser(link):
    news = ''
    try:
        soup = req_begin(link)
        article_body = soup.find("div", class_="news_body")
        for p in article_body.find_all("div"):
            p.extract()
        for p in article_body.find_all("br"):
            p.extract()
        for p in article_body.find_all("h2"):
            p.extract()
        news = article_body.get_text().replace('\n\n\n\n', '\n').replace('\n\n\n', '\n').replace('\n\n', '\n').replace('\n\r\n', '\n')
    except:
        pass

    return news