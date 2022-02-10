import os
import sys

SOURCE_DIR = os.path.dirname(__file__)
sys.path.append(SOURCE_DIR)

import uvicorn
from asgiref.wsgi import WsgiToAsgi

from app import create_app
from core.config import FLASK_HOST, FLASK_PORT
from core.logger import LOGGING

asgi_app = WsgiToAsgi(create_app())


if __name__ == '__main__':
    uvicorn.run(
        'asgi:asgi_app',
        host=FLASK_HOST,
        port=FLASK_PORT,
        log_config=LOGGING
    )
