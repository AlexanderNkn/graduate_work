import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = 'voice_assistant'
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    assistant_host: str = 'http://127.0.0.1'
    assistant_port: int = 8000
    assistant_base_url: str = '/assistant-api/v1'

    movies_host: str = 'http://127.0.0.1'
    movies_port: int = 80
    movies_base_url: str = '/movies-api/v1'

    auth_host: str = 'http://127.0.0.1'
    auth_port: int = 80
    auth_base_url: str = '/auth-api/v1'
    enable_authorization: int = 0

    jaeger_repoting_host: str = 'http://127.0.0.1'
    jaeger_repoting_port: int = 6831

    class Config:
        fields = {
            'project_name': {'env': 'PROJECT_NAME'},
            'assistant_host': {'env': 'ASSISTANTAPI_HOST'},
            'assistant_port': {'env': 'ASSISTANTAPI_PORT'},
            'assistant_base_url': {'env': 'ASSISTANTAPI_BASE_URL'},
            'movies_host': {'env': 'MOVIESAPI_HOST'},
            'movies_port': {'env': 'MOVIESAPI_PORT'},
            'movies_base_url': {'env': 'MOVIESAPI_BASE_URL'},
            'auth_host': {'env': 'AUTH_HOST'},
            'auth_port': {'env': 'AUTH_PORT'},
            'auth_base_url': {'env': 'AUTH_BASE_URL'},
            'enable_authorization': {'env': 'ENABLE_AUTHORIZATION'},
            'jaeger_repoting_host': {'env': 'JAEGER_REPORTING_HOST'},
            'jaeger_repoting_port': {'env': 'JAEGER_REPORTING_PORT'},
        }


settings = Settings()
