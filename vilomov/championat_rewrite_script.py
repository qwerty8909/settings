# загружаем необходимые модули и библиотеки
import openai
import random
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from deep_translator import GoogleTranslator

key_words = ['спартак', 'северсталь']
openai.api_key = ("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")

# проверяем доступность сайта
req = Request(
    url='https://www.championat.com/news/bets/1.html',
    headers={'User-Agent': 'Mozilla/5.0'}
)
website_url = urlopen(req).read()
soup = BeautifulSoup(website_url, 'lxml')

links = []
news_link = soup.find_all('div', class_='news-item')
for news in news_link:
    links.append(
        {
            'link': 'https://www.championat.com' + news.find('a').get('href'),
            'text': news.find('a').get_text()  # .lower().replace('«', '').replace('»', '').replace('— ', '')
        })
df1 = pd.DataFrame(links)
df2 = pd.DataFrame()

key_words = [item.lower() for item in key_words]
df1.text = [item.lower() for item in df1.text]
for line in df1.text:
    if all(word in line for word in key_words):
        df0 = df1[df1.text.str.contains(line)]
        df2 = pd.concat([df2, df0], axis=0)

# проверяем доступность сайта
news = ''
text = ''
for link in sorted(df2.link, key=lambda _: random.random()):
    if len(news) < 4000:
        req = Request(
            url=link,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        website_url = urlopen(req).read()
        soup = BeautifulSoup(website_url, 'lxml')

        # Extract the title of the article
        title = soup.find("div", class_="article-head__title").text.strip() + ". "

        # Extract the text of the article
        article_body = soup.find("div",
                                 class_="article-content js-content-banners-wrapper js-copyright-content "
                                        "js-loyalty-article-content")

        # Check the last p tags for the presence of a tags
        for p in article_body.find_all("b")[-5:]:
            if p.find("a"):
                p.extract()

        for td in article_body.find_all('p', class_=None):
            news += str(td.text) + ' '
        news += '\n'

with open('gpt_rewrite_in.txt', 'w', encoding="utf-8") as file:
    for item in news.split('\n'):
        translated_en = GoogleTranslator(source='ru', target='en').translate(item)
        file.write(translated_en + '\n')

with open('gpt_rewrite_in.txt', 'r') as file:
    file_contents = file.read()

with open('gpt_rewrite_prompt.txt', 'r') as file:
    file_prompt = file.read()

content = file_contents.replace('\'', '').replace('\n', ' ').replace('"', ' ').replace("'", " ") \
    .replace('(', '').replace(')', '').replace('  ', ' ').replace(' .', '.')
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
with open('gpt_rewrite_out.txt', 'w', encoding="utf-8") as file:
    file.write(translated_ru)
