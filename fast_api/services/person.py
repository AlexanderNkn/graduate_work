from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic_db import ElasticStorage, get_elastic
from db.redis_db import RedisStorage, get_redis
from db.storage import CacheStorage, RemoteStorage
from models.person import PersonDetailedDTO
from services.base import BaseService


class PersonService(BaseService):
    pass


@lru_cache()
def get_person_service(
    elastic: AsyncElasticsearch = Depends(get_elastic), redis: Redis = Depends(get_redis)
) -> PersonService:
    storage: RemoteStorage = RemoteStorage(ElasticStorage(elastic))
    cache: CacheStorage = CacheStorage(RedisStorage(redis))
    return PersonService(index='persons', model=PersonDetailedDTO, storage=storage, cache=cache)
