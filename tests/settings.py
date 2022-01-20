import os

from pydantic import BaseSettings, Field

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

FASTAPI_HOST = os.getenv('FASTAPI_HOST', '127.0.0.1')
FASTAPI_PORT = int(os.getenv('FASTAPI_PORT', 8000))
BASE_URL = os.getenv('BASE_URL', '/api/v1')


class TestSettings(BaseSettings):
    elastic_url: str = Field(f'{ELASTIC_HOST}:{ELASTIC_PORT}')
    redis_url: str = Field(f'{REDIS_HOST}:{REDIS_PORT}')
    service_url: str = Field(f'{FASTAPI_HOST}:{FASTAPI_PORT}{BASE_URL}', description='url for fastapi service')


settings = TestSettings()
