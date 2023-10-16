# Define table and column information
TABLE_GAMES = 'st_games'
COLUMNS_GAMES = {
        'id': 'VARCHAR(15) NULL PRIMARY KEY',
        'dt': 'TIMESTAMP NULL',
        'game': 'VARCHAR(30) NULL',
        'com1': 'VARCHAR(50) NULL',
        'com2': 'VARCHAR(50) NULL',
        'p1': 'FLOAT',
        'x': 'FLOAT',
        'p2': 'FLOAT'
}

TABLE_PROGNOZIST = 'st_prognozist'
COLUMNS_PROGNOZIST = {
        'link': 'VARCHAR(100) NULL PRIMARY KEY',
        'com1': 'VARCHAR(50) NULL',
        'com2': 'VARCHAR(50) NULL',
        'dt': 'TIMESTAMP NULL',
        'tips': 'VARCHAR(10000) NULL'
}

TABLE_ARTICLES = 'st_articles'
COLUMNS_ARTICLES = {
        'link': 'VARCHAR(200) NULL PRIMARY KEY',
        'com1': 'VARCHAR(50) NULL',
        'com2': 'VARCHAR(50) NULL',
        'dt': 'TIMESTAMP NULL'
}

#################################game commands################################
create_table_games = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_GAMES} (
        {', '.join([f'{col} {type}' for col, type in COLUMNS_GAMES.items()])}
    )
"""

delete_elements_games = f'''DELETE FROM {TABLE_GAMES} WHERE dt < %s;'''

insert_elements_games = f"""
    INSERT INTO {TABLE_GAMES} ({', '.join(COLUMNS_GAMES.keys())})
    VALUES (%s, TO_TIMESTAMP(%s) AT TIME ZONE 'Europe/Moscow', %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE
    SET {', '.join([f'{col} = EXCLUDED.{col}' for col in COLUMNS_GAMES.keys()])};
"""

#################################prognozist commands################################
create_table_prognozist = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_PROGNOZIST} (
        {', '.join([f'{col} {type}' for col, type in COLUMNS_PROGNOZIST.items()])}
    )
"""

delete_elements_prognozist = f'''DELETE FROM {TABLE_PROGNOZIST} WHERE dt < %s;'''

insert_elements_prognozist = f"""
    INSERT INTO {TABLE_PROGNOZIST} ({', '.join(COLUMNS_PROGNOZIST.keys())})
    VALUES (%s, %s, %s, TO_TIMESTAMP(%s) AT TIME ZONE 'Europe/Moscow', %s)
    ON CONFLICT (link) DO UPDATE
    SET {', '.join([f'{col} = EXCLUDED.{col}' for col in COLUMNS_PROGNOZIST.keys()])};
"""

#################################articles commands################################
create_table_articles = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_ARTICLES} (
        {', '.join([f'{col} {type}' for col, type in COLUMNS_ARTICLES.items()])}
    )
"""

delete_elements_articles = f'''DELETE FROM {TABLE_ARTICLES} WHERE dt < %s;'''

insert_elements_articles = f"""
    INSERT INTO {TABLE_ARTICLES} ({', '.join(COLUMNS_ARTICLES.keys())})
    VALUES (%s, %s, %s, TO_TIMESTAMP(%s) AT TIME ZONE 'Europe/Moscow')
    ON CONFLICT (link) DO UPDATE
    SET {', '.join([f'{col} = EXCLUDED.{col}' for col in COLUMNS_ARTICLES.keys()])};
"""
