import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass

import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from multidict import CIMultiDictProxy

from .settings import settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=settings.elastic_url)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
def send_data_to_elastic(es_client: AsyncElasticsearch):
    """Sends test data to Elastic before test, then deletes data after test

    Example data
        [
            {
                "index": "test_movies",
                "_id": "ac58403b-7070-4dcc-8e53-fa2d2d2284ab",
                "id": "ac58403b-7070-4dcc-8e53-fa2d2d2284ab",
                "title": "Video Killed the Radio Star",
                "imdb_rating": 7,
                ...
            },
            {
                ...
            }
        ]
    """
    @asynccontextmanager
    async def inner(data: list[dict]):
        await async_bulk(client=es_client, actions=data)
        try:
            yield
        finally:
            data_to_delete = (dict({'_op_type': 'delete'}, **doc) for doc in data)
            await async_bulk(client=es_client, actions=data_to_delete)
    return inner


@pytest_asyncio.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f'{settings.service_url}{method}'
        async with session.get(url, params=params) as response:
            return HTTPResponse(
              body=await response.json(),
              headers=response.headers,
              status=response.status,
            )
    return inner
