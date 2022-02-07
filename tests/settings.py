import os
from datetime import timedelta

from pydantic import BaseSettings, Field

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6399))

POSTGRE_HOST = os.getenv('POSTGRE_HOST', 'localhost')
POSTGRE_PORT = int(os.getenv('POSTGRE_PORT', 5433))
POSTGRE_NAME = os.getenv('POSTGRE_NAME', 'auth_database_test')
POSTGRE_USER = os.getenv('POSTGRE_USER', 'postgre')
POSTGRE_PASSWORD = os.getenv('POSTGRE_USER', 'postgre')
POSTGRE_OPTIONS = os.getenv('POSTGRE_OPTIONS', '-c search_path=users')

FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
BASE_URL = os.getenv('BASE_URL', '/api/v1')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 5))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 20))


class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str = Field(JWT_SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = Field(JWT_ACCESS_TOKEN_EXPIRES)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = Field(JWT_REFRESH_TOKEN_EXPIRES)


class PostgreSettings(BaseSettings):
    host: str = Field(POSTGRE_HOST)
    port: int = Field(POSTGRE_PORT)
    dbname: str = Field(POSTGRE_NAME)
    password: str = Field(POSTGRE_PASSWORD)
    user: str = Field(POSTGRE_USER)
    options: str = Field(POSTGRE_OPTIONS)


class TestSettings(BaseSettings):
    dsn: PostgreSettings = Field(PostgreSettings())
    jwt: JWTSettings = Field(JWTSettings())
    redis_url: str = Field(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    service_url: str = Field(f"postgresql://{POSTGRE_USER}:{POSTGRE_PASSWORD}" +
                             f"@{POSTGRE_HOST}:{POSTGRE_PORT}/{POSTGRE_NAME}"
                             , description='url for auth service')


settings = TestSettings()
