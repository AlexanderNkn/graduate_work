from functools import lru_cache

from fastapi import Depends
from aioredis import Redis
from db.elastic_db import get_elastic
from db.redis_db import get_redis
from elasticsearch import AsyncElasticsearch
from models.genre import GenreDetailedDTO

from services.base import BaseService


class GenreService(BaseService):
    pass


@lru_cache()
def get_genre_service(elastic: AsyncElasticsearch = Depends(get_elastic),
                      redis: Redis = Depends(get_redis)) -> GenreService:
    return GenreService(index='genres', model=GenreDetailedDTO, storage=elastic, cache=redis)
