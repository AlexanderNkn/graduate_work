from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonDetailedDTO

from .base import BaseService


class PersonService(BaseService):
    pass


@lru_cache()
def get_person_service(elastic: AsyncElasticsearch = Depends(get_elastic),
                       redis: Redis = Depends(get_redis)) -> PersonService:
    return PersonService(index='persons', model=PersonDetailedDTO, elastic=elastic, redis=redis)
