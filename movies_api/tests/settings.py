import os

from pydantic import BaseSettings, Field

REDIS_HOST = os.getenv('REDIS_HOST_TEST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT_TEST', 6389))

ELASTIC_HOST = os.getenv('ELASTIC_HOST_TEST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT_TEST', 9210))

MOVIESAPI_HOST = os.getenv('MOVIESAPI_HOST', 'http://127.0.0.1')
MOVIESAPI_PORT = int(os.getenv('MOVIESAPI_PORT', 80))
BASE_URL = os.getenv('BASE_URL', '/movies-api/v1')


class TestSettings(BaseSettings):
    elastic_url: str = Field(f'{ELASTIC_HOST}:{ELASTIC_PORT}')
    redis_url: str = Field(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    service_url: str = Field(f'{MOVIESAPI_HOST}:{MOVIESAPI_PORT}{BASE_URL}', description='url for movies_api service')


settings = TestSettings()
