import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent

BASE_URL = 'https://line02w.bk6bba-resources.com/events/listBase?lang=ru&scopeMarket=1600'
HEADERS = {'User-Agent': UserAgent().random}


# Функция для выполнения HTTP-запроса с обработкой ошибок
def make_request(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def parse_data(url):
    result_list = []
    response = make_request(url)
    if response:
        soup = BeautifulSoup(response.content, 'lxml')
        json_data = soup.p.get_text()
        data = json.loads(json_data)
        # Извлечение данных
        events_index = {item.get('id'): item for item in data['events']}
        factor_index = {item.get('e'): item for item in data['customFactors']}

        # Перебираем liveEventInfos и используем индекс для поиска событий
        for item in data['liveEventInfos']:
            if 'scoreFunction' in item and item['scoreFunction'] == 'Basketball' and len(item['scores']) > 1 and len(item['scores'][1]) == 4:
                event = events_index.get(item.get('eventId'))
                factor = factor_index.get(item.get('eventId'))
                if event and factor:
                    team1 = event['team1']
                    team2 = event['team2']
                    timer = item['timerSeconds']
                    score_total = int(item['scores'][0][0]['c1']) + int(item['scores'][0][0]['c2'])
                    if 2400 < item['timerSeconds'] < 2800:
                        score_predict = round(score_total / timer * 2880)
                    elif 1800 < item['timerSeconds'] < 2160:
                        score_predict = round(score_total / timer * 2400)
                    elif 2160 < item['timerSeconds'] < 2400:
                        score_predict = f'{round(score_total / timer * 2400)} или {round(score_total / timer * 2880)}'
                    else:
                        continue
                    link = f"https://www.fon.bet/live/basketball/{event['sportId']}/{event['id']}/"
                    print(
                        f"{team1} - {team2}\n"
                        f"Cчет: {score_total}. - Прогноз: {score_predict}. - Время: {timer//60}:{timer%60}\n\n"
                        # f"Ссылка: {link}\n\n"
                    )

    return result_list


# Основная функция для выполнения запросов и обработки данных
def main():
    parse_data(BASE_URL)


if __name__ == "__main__":
    main()
