import os

from pydantic import BaseSettings, Field

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6389))

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9210))

FASTAPI_HOST = os.getenv('FASTAPI_HOST', 'http://127.0.0.1')
FASTAPI_PORT = int(os.getenv('FASTAPI_PORT', 80))
BASE_URL = os.getenv('BASE_URL', '/movies-api/v1')


class TestSettings(BaseSettings):
    elastic_url: str = Field(f'{ELASTIC_HOST}:{ELASTIC_PORT}')
    redis_url: str = Field(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    service_url: str = Field(f'{FASTAPI_HOST}:{FASTAPI_PORT}{BASE_URL}', description='url for fastapi service')


settings = TestSettings()
