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
        soup = req_begin('https://stavki-online.info/prognozy-na-matchi/')
        news_link = soup.find_all('h4')[:15]
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
        article_body = soup.find("div", class_="fusion-column-wrapper fusion-column-has-shadow fusion-flex-column-wrapper-legacy")
        for p in article_body.find_all("div", class_="reading-box")[-3:]:
            if p.find('a'):
                p.extract()
        for td in article_body.find_all('p', class_=None)[:-1]:
            news += str(td.text).replace('\xa0', '').replace('\n', '') + '\n'
    except:
        pass

    return news
