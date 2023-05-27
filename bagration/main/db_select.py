import sqlite3


def sqlite_request(request):
    con = sqlite3.connect(r"C:\Users\vitalii\IdeaProjects\settings\test.db")
    cur = con.cursor()
    cur.execute(request)
    result = cur.fetchall()
    con.commit()
    con.close()
    return result


def select_id():
    result = sqlite_request("SELECT id FROM bagration;")
    return result


def select_account(tg_id):
    result = sqlite_request(f"SELECT account FROM bagration WHERE id = {tg_id};")[0][0]
    return result


def select_button(column, tg_id):
    result = sqlite_request(f"SELECT {column} FROM bagration WHERE id = {tg_id};")
    return result


def update_id(tg_id, account):
    sqlite_request(f"UPDATE bagration SET id = NULL WHERE id = {tg_id}")
    sqlite_request(f"UPDATE bagration SET id = {tg_id} WHERE account = {account}")


def select_address(account):
    result = sqlite_request(f'SELECT address FROM bagration WHERE account = {account};')[0][0]
    return result


def select_indicator(button, tg_id):
    result = sqlite_request(f"SELECT {button} FROM bagration  WHERE id = {tg_id}")[0][0]
    return result


def update_indicator(button, text, tg_id):
    result = sqlite_request(f"UPDATE bagration SET {button} = {text} WHERE id = {tg_id}")
    return result
