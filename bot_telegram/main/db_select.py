import sqlite3


def sqlite_request(request, params=()):
    with sqlite3.connect(r"C:\Users\vitalii\IdeaProjects\settings\test.db") as con:
        cur = con.cursor()
        cur.execute(request, params)
        result = cur.fetchall()
        con.commit()
    return result


def check_account(account):
    result = sqlite_request("SELECT count(account) FROM outline_tg WHERE account = (?);", (account,))
    return result[0][0]


def insert_data(account, payment):
    sqlite_request("INSERT INTO outline_tg (account, payment) VALUES (?, ?);", (account, payment))


def select_indicator_button(column, account):
    result = sqlite_request(f"SELECT {column} FROM bagration WHERE account = {account};")
    return result


def select_account_button(tg_id):
    result = sqlite_request(f"SELECT account FROM user_tg WHERE id = {tg_id};")
    return result


def select_account_address(account):
    result = sqlite_request(f"SELECT address FROM bagration WHERE account = {account};")
    return result[0][0]


def update_id(tg_id, account):
    sqlite_request(f"UPDATE bagration SET id = NULL WHERE id = {tg_id}")
    sqlite_request(f"UPDATE bagration SET id = {tg_id} WHERE account = {account}")


def select_address(account):
    result = sqlite_request(f'SELECT address FROM bagration WHERE account = {account};')
    return result[0][0]


def select_indicator(column, account):
    result = sqlite_request(f"SELECT {column} FROM bagration  WHERE account = {account}")
    return result[0][0]


def update_indicator(column, value, account):
    sqlite_request(f"UPDATE bagration SET {column} = {value} WHERE account = {account}")


def del_account(account, tg_id):
    sqlite_request(f"DELETE FROM user_tg WHERE account = {account} and id = {tg_id}")
