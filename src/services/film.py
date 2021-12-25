from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from models.film import Film

from .base import BaseService


class FilmService(BaseService):
    pass


@lru_cache()
def get_film_service(elastic: AsyncElasticsearch = Depends(get_elastic),) -> FilmService:
    return FilmService(index='movies', model=Film, elastic=elastic)
