from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic_db import ElasticStorage, get_elastic
from db.redis_db import RedisStorage, get_redis
from db.storage import CacheStorage, RemoteStorage
from models.genre import GenreDetailedDTO
from services.base import BaseService


class GenreService(BaseService):
    pass


@lru_cache()
def get_genre_service(
    elastic: AsyncElasticsearch = Depends(get_elastic), redis: Redis = Depends(get_redis)
) -> GenreService:
    storage: RemoteStorage = RemoteStorage(ElasticStorage(elastic))
    cache: CacheStorage = CacheStorage(RedisStorage(redis))
    return GenreService(index='genres', model=GenreDetailedDTO, storage=storage, cache=cache)
