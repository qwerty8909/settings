import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

HEADERS = {
    'Cookie': 'zen_sso_checked=1'
}

MONTH_DICT = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
    'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
    'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
}

STOP_WORDS = {
    "в", "на", "по", "с", "за", "у", "к", "о", "от", "до", "перед", "под", "над", "через", "между",
    "и", "или", "да", "либо", "же", "то", "а", "но", "если", "как", "что", "потому что",
    "чтобы", "ли", "потому", "чтоб", "пока", "пока не", "еще", "во", "со", "про", "не", "из",
    "без", "для",
    "игр", "игры", "игре", "игру", "играх"
}

def make_request(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def parse_data(url):
    response = make_request(url)
    soup = BeautifulSoup(response.content, 'lxml')
    json_str = soup.find('p').get_text()
    data = json.loads(json_str)
    return data

def get_datetime(data_list, current_date):
    if "вчера" in data_list['time']:
        date = current_date - timedelta(days=1)
        time_str = data_list['time'].split()[-1]
    elif len(data_list['time'].split("в")) > 1:
        date_str, time_str = data_list['time'].split(" в ")
        day_str, month_str = date_str.split()
        day = int(day_str)
        month = MONTH_DICT[month_str]
        year = current_date.year
        if current_date.month < month:
            year -= 1
        date = datetime(year, month, day)
    else:
        date = current_date
        time_str = data_list['time'].split()[-1]

    updated_timestamp = date.strftime("%Y-%m-%d") + " " + time_str
    return datetime.strptime(updated_timestamp, "%Y-%m-%d %H:%M")

def process_text(text):
    text = text.lower().replace('-', ' ')
    text = ''.join(char for char in text if char.isalpha() or char.isspace())
    text_words = text.split()
    filtered_words = [word for word in text_words if word not in STOP_WORDS]
    new_text = ' '.join(filtered_words)
    return new_text

current_date = datetime.now()
one_month_ago = current_date - timedelta(days=30)
combined_text = ''

for i in range(50):
    data = parse_data(f'https://dzen.ru/news/search?ajax=1&issue_tld=ru&text=игра&flat=1&&p={i}')
    if 'data' in data and 'stories' in data['data']:
        for story in data['data']['stories']:
            if 'docs' in story and story['docs']:
                data_list = story['docs'][0]
                article_timestamp = get_datetime(data_list, current_date)

                if article_timestamp >= one_month_ago:
                    combined_text += ' '.join(item['text'] for item in data_list['text'] + data_list['title']) + ' '

combined_text = process_text(combined_text)
words = combined_text.split()
word_counts = Counter(words)
top_words = word_counts.most_common(50)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(top_words))

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()