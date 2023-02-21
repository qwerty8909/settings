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
        soup = req_begin('https://www.liveresult.ru/tips')
        news_link = soup.find_all('div', class_='tips-list-tip')
        for news in news_link:
            links.append(
                {
                    'link': 'https://www.liveresult.ru' + news.find('a').get('href'),
                    'text': news.find('a').get_text().strip().replace('\n', ' - ')
                })
    except:
        pass

    return links


def site_parser(link):
    news = ''
    try:
        soup = req_begin(link)
        article_body = soup.find("div", class_="tip-page-tex article-text mb-3")
        for td in article_body.find_all('p', class_=None):
            news += str(td.text).replace('\xa0', '').replace('\n', '') + '\n'
    except:
        pass

    return news
