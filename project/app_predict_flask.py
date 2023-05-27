import openai
import random
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from flask import Flask, request, render_template
from deep_translator import GoogleTranslator

app = Flask(__name__, template_folder='C:/Users/vitalii/IdeaProjects/settings/vilomov')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        with open('gpt_rewrite_out.txt', 'w') as file:
            file.write(' ')

        key_words = user_input.split()
        openai.api_key = ("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")

        # проверяем доступность сайта
        games_meta = ['futbol', 'hokkey', 'basketbol', 'tennis']
        games = ['football', 'hockey', 'basketball', 'tennis']
        links = []

        for game in games_meta:
            req = Request(
                url='https://metaratings.ru/prognozy/' + game,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            website_url = urlopen(req).read()
            soup = BeautifulSoup(website_url, 'lxml')
            soup = soup.find('div', class_='TipsList_TipsList__dDOki')
            news_link = soup.find_all('div', class_='TipsList_TipsBoxTitle__sCRne')
            for news in news_link:
                links.append(
                    {
                        'link': 'https://metaratings.ru' + news.find('a').get('href'),
                        'text': news.find('a').get_text()
                        # .lower().replace('«', '').replace('»', '').replace('— ', '')
                    })

        for game in games:
            req = Request(
                url='https://odds.ru/' + game + '/forecasts/',
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            website_url = urlopen(req).read()
            soup = BeautifulSoup(website_url, 'lxml')
            news_link = soup.find_all('div', class_='forecasts-post__title')
            for news in news_link:
                links.append(
                    {
                        'link': 'https://odds.ru' + news.find('a').get('href'),
                        'text': news.find('a').get_text()
                        # .lower().replace('«', '').replace('»', '').replace('— ', '')
                    })

        for game in games:
            req = Request(
                url='https://www.vseprosport.ru/news/' + game,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            website_url = urlopen(req).read()
            soup = BeautifulSoup(website_url, 'lxml')
            news_link = soup.find_all('a', class_='forecast no-link-text small-text p-10')[:12]
            for news in news_link:
                links.append(
                    {
                        'link': 'https://www.vseprosport.ru' + news.get('href'),
                        'text': news.find('div', class_='forecast__text').get_text()
                    })

        for game in games:
            req = Request(
                url='https://stavkiprognozy.ru/prognozy/' + game + '/',
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            website_url = urlopen(req).read()
            soup = BeautifulSoup(website_url, 'lxml')
            news_link = soup.find_all('div', class_='box-item-body announce-item-body')
            for news in news_link:
                links.append(
                    {
                        'link': 'https://stavkiprognozy.ru' + news.find('a').get('href'),
                        'text': news.find_next('div', class_='single-announce-team-title').get_text()
                    })

        req = Request(
            url='https://www.championat.com/news/bets/1.html',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        website_url = urlopen(req).read()
        soup = BeautifulSoup(website_url, 'lxml')
        news_link = soup.find_all('div', class_='news-item')
        for news in news_link:
            links.append(
                {
                    'link': 'https://www.championat.com' + news.find('a').get('href'),
                    'text': news.find('a').get_text()  # .lower().replace('«', '').replace('»', '').replace('— ', '')
                })

        req = Request(
            url='https://www.liveresult.ru/tips',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        website_url = urlopen(req).read()
        soup = BeautifulSoup(website_url, 'lxml')
        news_link = soup.find_all('div', class_='tips-list-tip')
        for news in news_link:
            links.append(
                {
                    'link': 'https://www.liveresult.ru' + news.find('a').get('href'),
                    'text': news.find('a').get_text().strip().replace('\n', ' - ')
                })

        req = Request(
            url='https://stavki-online.info/prognozy-na-matchi/',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        website_url = urlopen(req).read()
        soup = BeautifulSoup(website_url, 'lxml')
        news_link = soup.find_all('h4')[:15]  # ('div', class_='recent-posts-content')
        for news in news_link:
            links.append(
                {
                    'link': news.find('a').get('href'),
                    'text': news.find('a').get_text()
                })

        req = Request(
            url='https://ironbets.ru/prognozy/',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        website_url = urlopen(req).read()
        soup = BeautifulSoup(website_url, 'lxml')
        news_link = soup.find_all('div', class_='post-card__title')
        for news in news_link:
            links.append(
                {
                    'link': news.find('a').get('href'),
                    'text': news.find('a').get_text()
                })

        df1 = pd.DataFrame(links)
        df2 = pd.DataFrame()
        key_words = [item.lower() for item in key_words]
        df1.text = [item.lower() for item in df1.text]
        for line in df1.text:
            if all(word in line for word in key_words):
                df0 = df1[df1.text.str.contains(line)]
                df2 = pd.concat([df2, df0], axis=0).drop_duplicates()

        news = ''
        for link in sorted(df2.link, key=lambda _: random.random()):
            a_len = 0
            if len(news) < 4000:
                req = Request(
                    url=link,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                website_url = urlopen(req).read()
                soup = BeautifulSoup(website_url, 'lxml')

                if 'metaratings.ru' in link:
                    article_body = soup.find("article", class_=None)
                    for p in article_body.find_all("p")[-3:]:
                        if p.find("b"):
                            p.extract()
                    for td in article_body.find_all('p', class_=None):
                        a_len += len(str(td.text))
                        if a_len < 3000:
                            news += str(td.text) + ' '
                    news += '\n'

                if 'championat.com' in link:
                    article_body = soup.find("div",
                                             class_="article-content js-content-banners-wrapper js-copyright-content "
                                                    "js-loyalty-article-content")
                    for p in article_body.find_all("b")[-5:]:
                        if p.find("a"):
                            p.extract()
                    for td in article_body.find_all('p', class_=None):
                        news += str(td.text) + ' '
                    news += '\n'

                if 'odds.ru' in link:
                    article_inherit = soup.find("div", class_="post-inherit__description").get_text()
                    article_body = soup.find("div", class_="forecast-text")
                    news += article_inherit.replace('\n', ' ').replace('\t', ' ').replace('   ', '')
                    for p in article_body.find_all("b")[-3:]:
                        if p.find("a"):
                            p.extract()
                    for td in article_body.find_all('p', class_=None):
                        news += str(td.text.replace('\n', ' ').replace('«Фонбет»', '')) + ' '
                    news += '\n'

                if 'sports.ru' in link:
                    article_body = soup.find("div", class_="article__content js-mediator-article")
                    for p in article_body.find_all("p")[-3:]:
                        if p.find("i"):
                            p.extract()
                    for td in article_body.find_all('p', class_=None):
                        news += str(td.text) + ' '
                    news += '\n'

                if 'liveresult.ru' in link:
                    article_body = soup.find("div", class_="tip-page-tex article-text mb-3")
                    for td in article_body.find_all('p'):
                        news += str(td.text.replace('\xa0', '').replace('\n', ' ')) + ' '
                    news += '\n'

                if 'stavki-online.info' in link:
                    article_body = soup.find("div",
                                             class_="fusion-column-wrapper fusion-column-has-shadow "
                                                    "fusion-flex-column-wrapper-legacy")
                    for p in article_body.find_all("div", class_="reading-box")[-3:]:
                        if p.find('a'):
                            p.extract()
                    for td in article_body.find_all('p', class_=None)[:-1]:
                        news += str(td.text) + ' '
                    news += '\n'

                if 'ironbets.ru' in link:
                    article_body = soup.find("div", class_="entry-content")
                    for td in article_body.find_all('p'):
                        news += str(td.text.replace('Winline', '')) + ' '
                    news = news + '\n'

                if 'vseprosport.ru' in link:
                    article_body = soup.find("div", class_="white-radius mb-4")
                    for td in article_body.find_all('p'):
                        news += str(td.text) + '\n '
                    news = news + '\n'

                if 'stavkiprognozy.ru' in link:
                    article_body = soup.find("div", itemtype="http://schema.org/SportsEvent")
                    for td in article_body.find_all('p'):
                        news += str(td.text) + '\n '
                    news = news + '\n'

        with open('gpt_rewrite_in.txt', 'w', encoding="utf-8") as file:
            for item in news.split('\n'):
                translated_en = GoogleTranslator(source='ru', target='en').translate(item)
                file.write(translated_en + '\n')

        with open('gpt_rewrite_in.txt', 'r') as file:
            file_contents = file.read()

        with open('gpt_rewrite_prompt.txt', 'r') as file:
            file_prompt = file.read()

        content = file_contents.replace('\n', ' ').replace('\t', '').replace('"', '').replace("'", "") \
            .replace('(', '').replace(')', '').replace('  ', ' ').replace('   ', ' ').replace(' .', '.')
        results = openai.Completion.create(
            model="text-davinci-003",               # "text-davinci-003" "text-curie-001"
            prompt=file_prompt + content + '.\n',   # make the article in 650 words as sport news:
                                                    # make the advertising in 150 words for sporting event:
                                                    # summarize text in 600 words:
                                                    # shorten the article in 650 words:
            temperature=0.7,
            max_tokens=1500,
            top_p=1,
            best_of=1,
            frequency_penalty=0.5,
            presence_penalty=0,
            stop=["//#"]
        )
        response = dict(results)
        openai_response = response['choices']
        eng_text = openai_response[-1]['text']

        translated_ru = GoogleTranslator(source='en', target='ru').translate(eng_text)
        with open('gpt_rewrite_out.txt', 'w') as file:
            file.write(translated_ru)
    else:
        user_input = None

    with open('gpt_rewrite_out.txt', 'r') as f:
        output = f.read()


if __name__ == '__main__':
    app.run()
