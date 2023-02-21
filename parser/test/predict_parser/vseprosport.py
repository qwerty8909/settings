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
    games = ['football', 'hockey', 'basketball', 'tennis', 'boxing']

    try:
        for game in games:
            soup = req_begin('https://www.vseprosport.ru/news/' + game)
            news_link = soup.find_all('a', class_='forecast no-link-text small-text p-10')[:12]
            for news in news_link:
                links.append(
                    {
                        'link': 'https://www.vseprosport.ru' + news.get('href'),
                        'text': news.find('div', class_='forecast__text').get_text()
                    })
    except:
        pass

    return links


def site_parser(link):
    news = ''
    try:
        soup = req_begin(link)
        article_body = soup.find("div", class_="white-radius mb-4")
        for td in article_body.find_all('p'):
            news += str(td.text).replace('\n', '') + '\n'
    except:
        pass

    return news