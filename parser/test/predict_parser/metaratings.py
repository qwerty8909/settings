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
    games = ['futbol', 'hokkey', 'basketbol', 'tennis', 'mma']

    try:
        for game in games:
            soup = req_begin('https://metaratings.ru/prognozy/' + game + '/')
            soup = soup.find('div', class_='forecast-tabWrap').find_next('div', class_='')
            for p in soup.find_all("a", target="_blank")[-5:]:
                if p.find("span"):
                    p.extract()
            news_link = soup.find_all('a')
            for news in news_link:
                links.append(
                    {
                        'link': 'https://metaratings.ru' + news.get('href'),
                        'text': news.get_text()
                    })
    except:
        pass

    return links


def site_parser(link):
    news = ''
    try:
        soup = req_begin(link)
        article_body = soup.find("article", class_=None)
        for p in article_body.find_all("p")[-3:]:
            if p.find("b"):
                p.extract()
        for td in article_body.find_all('p', class_=None):
            news += str(td.text).replace('\n', '') + '\n'
    except:
        pass

    return news
