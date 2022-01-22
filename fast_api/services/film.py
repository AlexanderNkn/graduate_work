from functools import lru_cache

from fastapi import Depends

from aioredis import Redis
from db.elastic_db import get_elastic
from db.redis_db import get_redis
from elasticsearch import AsyncElasticsearch
from models.film import FilmDetailedDTO

from services.base import BaseService


class FilmService(BaseService):
    pass


@lru_cache()
def get_film_service(elastic: AsyncElasticsearch = Depends(get_elastic),
                     redis: Redis = Depends(get_redis)) -> FilmService:
    return FilmService(index='movies', model=FilmDetailedDTO, storage=elastic, cache=redis)
