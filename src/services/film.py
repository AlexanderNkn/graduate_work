from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from models.film import Film

from .utils import get_body


class FilmService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        doc = await self.elastic.get(index='movies', id=film_id)
        film = Film(**doc['_source'])
        return film or None

    async def get_films_by_params(self, **params) -> Optional[list[Film]]:
        body = get_body(**params)
        doc = await self.elastic.search(body=body, index='movies')
        film_list = [Film(**_doc['_source']) for _doc in doc['hits']['hits']]
        return film_list


@lru_cache()
def get_film_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
