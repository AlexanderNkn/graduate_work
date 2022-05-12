import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from api.v1 import voice_assistant
from core import config
from core.logger import LOGGING

logging.getLogger('backoff').addHandler(logging.StreamHandler())

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/assistant-api/openapi',
    redoc_url='/assistant-api/redoc',
    openapi_url='/assistant-api/openapi.json',
    default_response_class=HTMLResponse,
    description='Voice information about movies, genres and persons involved in movie making',
    version='1.0.0'
)

# static files
static_dir = os.path.join(config.BASE_DIR, 'static')
app.mount('/static', StaticFiles(directory=static_dir), name='static')


app.include_router(voice_assistant.router, prefix='/assistant-api/v1/voice', tags=['voice_search'])


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=config.ASSISTANTAPI_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )