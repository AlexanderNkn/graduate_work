import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'voice_assistant')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ASSISTANTAPI_HOST = os.getenv('ASSISTANTAPI_HOST', 'http://127.0.0.1')
ASSISTANTAPI_PORT = int(os.getenv('ASSISTANTAPI_PORT', 80))
ASSISTANTAPI_BASE_URL = os.getenv('ASSISTANTAPI_BASE_URL', '/assistant-api/v1')

MOVIESAPI_HOST = os.getenv('MOVIESAPI_HOST', 'http://127.0.0.1')
MOVIESAPI_PORT = int(os.getenv('MOVIESAPI_PORT', 80))
MOVIESAPI_BASE_URL = os.getenv('MOVIESAPI_BASE_URL', '/movies-api/v1')

AUTH_HOST = os.getenv('AUTH_HOST', 'http://127.0.0.1')
AUTH_PORT = int(os.getenv('AUTH_PORT', 80))
AUTH_BASE_URL = os.getenv('AUTH_BASE_URL', '/auth-api/v1')
ENABLE_AUTHORIZATION = int(os.getenv('ENABLE_AUTHORIZATION', 1))
