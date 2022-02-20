import os
from datetime import timedelta

from pydantic import BaseSettings, Field

SECRET_KEY_TEST = os.getenv('SECRET_KEY_TEST', 'super-secret')

REDIS_HOST_TEST = os.getenv('REDIS_HOST_TEST', '127.0.0.1')
REDIS_PORT_TEST = int(os.getenv('REDIS_PORT_TEST', 6389))

POSTGRES_HOST_TEST = os.getenv('POSTGRES_HOST_TEST', '127.0.0.1')
POSTGRES_PORT_TEST = int(os.getenv('POSTGRES_PORT_TEST', 5433))
POSTGRES_NAME_TEST = os.getenv('POSTGRES_NAME_TEST', 'auth_database_test')
POSTGRES_USER_TEST = os.getenv('POSTGRES_USER_TEST', 'postgres')
POSTGRES_PASSWORD_TEST = os.getenv('POSTGRES_PASSWORD_TEST', 1234)
POSTGRES_OPTIONS_TEST = os.getenv('POSTGRES_OPTIONS_TEST', '-c search_path=users')

FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
BASE_URL = os.getenv('BASE_URL', '/api/v1')

JWT_SECRET_KEY_TEST = os.getenv('JWT_SECRET_KEY_TEST', 'super-secret')
JWT_ACCESS_TOKEN_EXPIRES_TEST = os.getenv('JWT_ACCESS_TOKEN_EXPIRES_TEST_SECONDS', 300)  # 5 min
JWT_REFRESH_TOKEN_EXPIRES_TEST = os.getenv('JWT_REFRESH_TOKEN_EXPIRES_TEST_SECONDS', 1200)  # 20 min
JWT_ERROR_MESSAGE_KEY_TEST = os.getenv('JWT_ERROR_MESSAGE_KEY_TEST', 'message')

GOOGLE_CLIENT_ID_TEST = os.getenv('GOOGLE_CLIENT_ID_TEST', 'client_id')
GOOGLE_CLIENT_SECRET_TEST = os.getenv('GOOGLE_CLIENT_SECRET_TEST', 'client_secret')
REQUEST_LIMIT_PER_MINUTE = int(os.getenv('REQUEST_LIMIT_PER_MINUTE_TEST', 10000))
SENTRY_DSN = ''
SWAGGER_CONFIG = {}
JAEGER_CONFIG = {}


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str = Field(JWT_SECRET_KEY_TEST)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = Field(JWT_ACCESS_TOKEN_EXPIRES_TEST)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = Field(JWT_REFRESH_TOKEN_EXPIRES_TEST)
    JWT_ERROR_MESSAGE_KEY: str = Field(JWT_ERROR_MESSAGE_KEY_TEST)


class OAuthGoogleSettings(BaseSettings):
    GOOGLE_CLIENT_ID: str = Field(GOOGLE_CLIENT_ID_TEST)
    GOOGLE_CLIENT_SECRET: str = Field(GOOGLE_CLIENT_SECRET_TEST)
    SECRET_KEY: str = Field(SECRET_KEY_TEST)


class PostgresSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = Field(
        f'postgresql+psycopg2://{POSTGRES_USER_TEST}:{POSTGRES_PASSWORD_TEST}'
        f'@{POSTGRES_HOST_TEST}:{POSTGRES_PORT_TEST}/{POSTGRES_NAME_TEST}', description='url for auth service'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True


class RedisSettings(BaseSettings):
    CACHE_TYPE: str = Field('RedisCache')
    CACHE_REDIS_URL: str = Field(f'redis://{REDIS_HOST_TEST}:{REDIS_PORT_TEST}')
