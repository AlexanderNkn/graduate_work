import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from api.v1 import voice_assistant
from core.config import settings
from core.logger import LOGGING

logging.getLogger('backoff').addHandler(logging.StreamHandler())

app = FastAPI(
    title=settings.project_name,
    docs_url='/assistant-api/openapi',
    redoc_url='/assistant-api/redoc',
    openapi_url='/assistant-api/openapi.json',
    default_response_class=HTMLResponse,
    description='Voice assistant API to search information about films',
    version='1.0.0'
)

# static files
static_dir = os.path.join(settings.base_dir, 'static')
app.mount('/static', StaticFiles(directory=static_dir), name='static')


app.include_router(voice_assistant.router, prefix='/assistant-api/v1/voice', tags=['voice_search'])


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.assistant_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
