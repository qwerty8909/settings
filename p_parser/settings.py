from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    host: str  # URL-адрес базы данных
    port: str  # Порт базы данных
    user: str  # Username пользователя базы данных
    password: str  # Пароль к базе данных


@dataclass
class Config:
    db: DatabaseConfig


def load_config(path: str | None) -> Config:
    load_dotenv()

    db = DatabaseConfig(
        database=os.getenv('DB_DATABASE'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

    return Config(db=db,)


SETTINGS = load_config('.env')
print(SETTINGS)
