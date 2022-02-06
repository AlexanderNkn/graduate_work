import os
from logging import config as logging_config
from datetime import timedelta

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

SWAGGER_CONFIG = {
    "headers": [
    ],
    "openapi": "3.0.2",
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/openapi/",
    "url_prefix": "/api",
}

PROJECT_NAME = os.getenv('PROJECT_NAME', 'auth')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6389))

POSTGRE_HOST = os.getenv('POSTGRE_HOST', 'localhost')
POSTGRE_PORT = int(os.getenv('POSTGRE_PORT', 5432))
POSTGRE_NAME = os.getenv('POSTGRE_NAME', 'movies_database')
POSTGRE_USER = os.getenv('POSTGRE_USER', 'postgre')
POSTGRE_PASSWORD = os.getenv('POSTGRE_PASSWORD', 'postgre')
POSTGRE_OPTIONS = os.getenv('POSTGRE_OPTIONS', '-c search_path=users')

FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
BASE_URL = os.getenv('BASE_URL', '/api/v1')

# CACHE_EXPIRE_IN_SECONDS = int(os.getenv('CACHE_EXPIRE_IN_SECONDS', 300))

JWT_SECRET_KEY = 'super-secret'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
