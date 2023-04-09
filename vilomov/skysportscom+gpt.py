# загружаем необходимые модули и библиотеки
import requests
import openai
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

openai.api_key = ("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")

# ищем последнюю новость
link = 'https://www.skysports.com/news-wire'
url = requests.get(link).text
soup = BeautifulSoup(url, 'lxml')
news_link = soup.find('div', class_='news-list__item news-list__item--show-thumb-bp30').find('a').get('href')

# Если нужно конкретную ссылку
# news_link = 'https://www.skysports.com/football/news/11095/12370963/subscribe-to-the-essential-football-podcast-from-sky-sports'

# парсим
news_url = requests.get(news_link).text
news_soup = BeautifulSoup(news_url, 'lxml')
news = ''
for td in news_soup.find('div', class_='sdc-article-body sdc-article-body--lead').parent.find_all('p', class_= None):
    news += str(td.text)

# отравляем на обработку в GPT
content = news.replace('\'', '').replace('"', ' ')
results = openai.Completion.create(
    model="text-davinci-003", # "text-davinci-003" "text-curie-001"
    prompt="shorten the article in 650 words: \n"+ content +"",
    temperature=0.7,
    max_tokens=600,
    top_p=1,
    best_of=1,
    frequency_penalty=0.5,
    presence_penalty=0,
    stop=["//#"]
)
response = dict(results)
openai_response = response['choices']
eng_text = openai_response[-1]['text']

# переводим и сохраняем в файл
translated = GoogleTranslator(source='en', target='ru').translate(eng_text)
with open('skysportscom+gpt.txt', 'w') as file:
    file.write(translated)