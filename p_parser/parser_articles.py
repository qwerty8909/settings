import datetime
import psycopg2
from settings import SETTINGS
import db_query
from articles_parsers import liveresult, metaratings, odds, stavkiprognozy

parsers = [liveresult, metaratings, odds, stavkiprognozy]
current_time = datetime.datetime.now()


# Функция для вставки данных в базу данных
def data_to_base(cursor, parser):
    result_list = parser.news_parser()
    print(f'{parser.__name__.split(".")[-1]}\t- {len(result_list)}')
    for value in result_list:
        link, com1, com2, dt = value
        # Вставка значений в таблицу
        cursor.execute(db_query.insert_elements_articles, (link, com1, com2, dt))


# Основная функция для выполнения запросов и обработки данных
def main():
    conn = psycopg2.connect(database=SETTINGS.db.database,
                            host=SETTINGS.db.host,
                            port=SETTINGS.db.port,
                            user=SETTINGS.db.user,
                            password=SETTINGS.db.password)
    conn.autocommit = False
    cursor = conn.cursor()
    # Создание таблицы, если она еще не существует
    cursor.execute(db_query.create_table_articles)
    # Удаление строк, где значение в столбце 'dt' меньше текущей даты и времени
    cursor.execute(db_query.delete_elements_articles, (current_time,))
    conn.commit()

    for parser in parsers:
        data_to_base(cursor, parser)
        conn.commit()
    # закрытие соединения
    conn.close()


if __name__ == "__main__":
    main()
