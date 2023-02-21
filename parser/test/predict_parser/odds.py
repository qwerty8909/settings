from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def req_begin(link):
    req = Request(
        url=link,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    website_url = urlopen(req).read()
    soup = BeautifulSoup(website_url, 'html.parser')
    return soup

def news_parser():
    links = []
    games = ['football', 'hockey', 'basketball', 'other']

    try:
        for game in games:
            soup = req_begin('https://odds.ru/' + game + '/forecasts/')
            news_link = soup.find_all('div', class_='forecasts-post__title')
            for news in news_link:
                links.append(
                    {
                        'link': 'https://odds.ru' + news.find('a').get('href'),
                        'text': news.find('a').get_text()
                    })
    except:
        pass

    return links


def site_parser(link):
    news = ''
    try:
        soup = req_begin(link)
        article_body = soup.find("div", class_="forecast-text")
        for p in article_body.find_all("b")[-3:]:
            if p.find("a"):
                p.extract()
        for td in article_body.find_all('p', class_=None):
            news += str(td.text).replace('\n', '') + '\n'
    except:
        pass

    return news
