import os

from pydantic import BaseSettings, Field

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6399))

POSTGRE_HOST = os.getenv('POSTGRE_HOST', 'localhost')
POSTGRE_PORT = int(os.getenv('POSTGRE_PORT', 5433))
POSTGRE_NAME = os.getenv('POSTGRE_NAME', 'movies_database')
POSTGRE_USER = os.getenv('POSTGRE_USER', 'postgre')
POSTGRE_PASSWORD = os.getenv('POSTGRE_USER', 'postgre')
POSTGRE_OPTIONS = os.getenv('POSTGRE_OPTIONS', '-c search_path=users')

FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
BASE_URL = os.getenv('BASE_URL', '/api/v1')


class PostgreSettings(BaseSettings):
    host: str = Field(POSTGRE_HOST)
    port: int = Field(POSTGRE_PORT)
    dbname: str = Field(POSTGRE_NAME)
    password: str = Field(POSTGRE_PASSWORD)
    user: str = Field(POSTGRE_USER)
    options: str = Field(POSTGRE_OPTIONS)


class TestSettings(BaseSettings):
    dsn: PostgreSettings
    redis_url: str = Field(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    service_url: str = Field(f'{FLASK_HOST}:{FLASK_PORT}{BASE_URL}', description='url for auth service')


settings = TestSettings()
