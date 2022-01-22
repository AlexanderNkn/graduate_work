from functools import lru_cache

from fastapi import Depends
from aioredis import Redis
from db.elastic_db import get_elastic
from db.redis_db import get_redis
from elasticsearch import AsyncElasticsearch
from models.person import PersonDetailedDTO

from services.base import BaseService


class PersonService(BaseService):
    pass


@lru_cache()
def get_person_service(elastic: AsyncElasticsearch = Depends(get_elastic),
                       redis: Redis = Depends(get_redis)) -> PersonService:
    return PersonService(index='persons', model=PersonDetailedDTO, storage=elastic, cache=redis)
