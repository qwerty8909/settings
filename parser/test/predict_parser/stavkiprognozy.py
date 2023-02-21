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
    games = ['football', 'hockey', 'basketball', 'tennis']

    try:
        for game in games:
            soup = req_begin('https://stavkiprognozy.ru/prognozy/' + game + '/')
            news_link = soup.find_all('div', class_='box-item-body announce-item-body')
            for news in news_link:
                links.append(
                    {
                        'link': 'https://stavkiprognozy.ru' + news.find('a').get('href'),
                        'text': news.find_next('div', class_='single-announce-team-title').get_text()
                    })
    except:
        pass

    return links


def site_parser(link):
    news = ''
    try:
        soup = req_begin(link)
        article_body = soup.find("div", itemtype="http://schema.org/SportsEvent")
        for td in article_body.find_all('p', class_=None):
            news += str(td.text).replace('\n', '') + '\n'
    except:
        pass

    return news
