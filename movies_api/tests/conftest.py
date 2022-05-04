from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator, Callable

import aiohttp
import pytest_asyncio
from aioredis import Redis, create_redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from multidict import CIMultiDictProxy

from .settings import settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture
async def es_client() -> AsyncGenerator[AsyncElasticsearch, None]:
    client = AsyncElasticsearch(hosts=settings.elastic_url)
    yield client
    await client.close()


@pytest_asyncio.fixture
async def redis_client() -> AsyncGenerator[Redis, None]:
    redis = await create_redis(address=settings.redis_url)
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
def clear_cache(redis_client: Redis):
    async def inner() -> None:
        await redis_client.flushall(async_op=True)
    return inner


@pytest_asyncio.fixture
def send_data_to_elastic(es_client: AsyncElasticsearch, clear_cache: Callable):
    """Sends test data to Elastic before test, then deletes data and cache after test.

    Not to remove cache for testing purposes should set with_clear_cache = False
    Example data:
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
    async def inner(data: list[dict], with_clear_cache: bool = True) -> AsyncGenerator[None, None]:
        await async_bulk(client=es_client, actions=data, refresh='wait_for')
        try:
            yield
        finally:
            data_to_delete = (dict({'_op_type': 'delete'}, **doc) for doc in data)
            await async_bulk(client=es_client, actions=data_to_delete)
            if with_clear_cache:
                await clear_cache()
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
