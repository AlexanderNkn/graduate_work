from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic_db import ElasticStorage, get_elastic
from db.redis_db import RedisStorage, get_redis
from db.storage import CacheStorage, RemoteStorage
from models.film import FilmDetailedDTO
from services.base import BaseService


class FilmService(BaseService):
    index = 'movies'
    model = FilmDetailedDTO


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic), redis: Redis = Depends(get_redis)
) -> FilmService:
    storage: RemoteStorage = RemoteStorage(ElasticStorage(elastic))
    cache: CacheStorage = CacheStorage(RedisStorage(redis))
    return FilmService(storage=storage, cache=cache)
