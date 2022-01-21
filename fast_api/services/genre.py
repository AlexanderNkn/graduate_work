from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import GenreDetailedDTO

from .base import BaseService


class GenreService(BaseService):
    pass


@lru_cache()
def get_genre_service(elastic: AsyncElasticsearch = Depends(get_elastic),
                      redis: Redis = Depends(get_redis)) -> GenreService:
    return GenreService(index='genres', model=GenreDetailedDTO, elastic=elastic, redis=redis)
