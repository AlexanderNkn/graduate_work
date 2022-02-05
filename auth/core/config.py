from logging import config as logging_config

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
