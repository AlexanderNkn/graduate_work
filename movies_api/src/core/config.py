import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6389))

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9210))

CACHE_EXPIRE_IN_SECONDS = int(os.getenv('CACHE_EXPIRE_IN_SECONDS', 300))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOVIESAPI_HOST = os.getenv('MOVIESAPI_HOST', 'http://127.0.0.1')
MOVIESAPI_PORT = int(os.getenv('MOVIESAPI_PORT', 80))
MOVIESAPI_BASE_URL = os.getenv('MOVIESAPI_BASE_URL', '/movies-api/v1')

AUTH_HOST = os.getenv('AUTH_HOST', 'http://127.0.0.1')
AUTH_PORT = int(os.getenv('AUTH_PORT', 80))
AUTH_BASE_URL = os.getenv('AUTH_BASE_URL', '/auth-api/v1')
ENABLE_AUTHORIZATION = int(os.getenv('ENABLE_AUTHORIZATION', 1))
