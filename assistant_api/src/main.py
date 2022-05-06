import logging

# import aioredis
import uvicorn
# from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import voice_assistant
from core import config
from core.logger import LOGGING

logging.getLogger('backoff').addHandler(logging.StreamHandler())

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/assistant-api/openapi',
    redoc_url='/assistant-api/redoc',
    openapi_url='/assistant-api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Information about assistant, genres and persons involved in movie making',
    version='1.0.0'
)


@app.on_event('startup')
async def startup():
    pass


@app.on_event('shutdown')
async def shutdown():
    pass

app.include_router(voice_assistant.router, prefix='/assistant-api/v1', tags=['film'])


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=config.ASSISTANTAPI_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
