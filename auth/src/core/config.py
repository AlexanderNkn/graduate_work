import os
from datetime import timedelta
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


PROJECT_NAME = os.getenv('PROJECT_NAME', 'auth')
SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6389))

POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
POSTGRES_NAME = os.getenv('POSTGRES_NAME', 'auth_database')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 1234)
POSTGRES_OPTIONS = os.getenv('POSTGRES_OPTIONS', '-c search_path=users')

FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
BASE_URL = os.getenv('BASE_URL', '/auth-api/v1')

JAEGER_REPORTING_HOST = os.getenv('JAEGER_REPORTING_HOST', '127.0.0.1')
JAEGER_REPORTING_PORT = int(os.getenv('JAEGER_REPORTING_PORT', 6831))

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret')
JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES_SECONDS', 1800)  # 30 min
JWT_REFRESH_TOKEN_EXPIRES = os.getenv('JWT_REFRESH_TOKEN_EXPIRES_SECONDS', 432000)  # 5 days
JWT_ERROR_MESSAGE_KEY = os.getenv('JWT_ERROR_MESSAGE_KEY', 'message')

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'client_id')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'client_secret')

YANDEX_CLIENT_ID = os.getenv('YANDEX_CLIENT_ID', 'client_id')
YANDEX_CLIENT_SECRET = os.getenv('YANDEX_CLIENT_SECRET', 'client_secret')

SENTRY_DSN = os.getenv('SENTRY_DSN', '')

REQUEST_LIMIT_PER_MINUTE = int(os.getenv('REQUEST_LIMIT_PER_MINUTE', 30))

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
    "url_prefix": "/auth-api",
}

JAEGER_CONFIG = {
    'sampler': {
        'type': 'const',
        'param': 1,
    },
    'local_agent': {
        'reporting_host': JAEGER_REPORTING_HOST,
        'reporting_port': JAEGER_REPORTING_PORT,
    },
    'logging': True,
}


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str = Field(JWT_SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = Field(JWT_ACCESS_TOKEN_EXPIRES)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = Field(JWT_REFRESH_TOKEN_EXPIRES)
    JWT_ERROR_MESSAGE_KEY: str = Field(JWT_ERROR_MESSAGE_KEY)


class OAuthSettings(BaseSettings):
    GOOGLE_CLIENT_ID: str = Field(GOOGLE_CLIENT_ID)
    GOOGLE_CLIENT_SECRET: str = Field(GOOGLE_CLIENT_SECRET)
    YANDEX_CLIENT_ID: str = Field(YANDEX_CLIENT_ID)
    YANDEX_CLIENT_SECRET: str = Field(YANDEX_CLIENT_SECRET)
    SECRET_KEY: str = Field(SECRET_KEY)


class PostgresSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = Field(
        f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}', description='url for auth service'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    SQLALCHEMY_ENGINE_OPTIONS: dict = {'pool_pre_ping': True, 'pool_recycle': 300, }


class RedisSettings(BaseSettings):
    CACHE_REDIS_URL: str = Field(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    CACHE_TYPE: str = Field('RedisCache')
