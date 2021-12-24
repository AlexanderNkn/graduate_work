from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends, Query

from db.elastic import get_elastic
from models.genre import Genre

from .utils import get_body


class GenreService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._get_genre_from_elastic(genre_id)
        return genre or None

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        doc = await self.elastic.get(index='genres', id=genre_id)
        return Genre(**doc['_source'])

    async def get_genres_by_params(self, **params) -> Optional[list[Genre]]:
        body = get_body(**params)
        docs = await self.elastic.search(index='genres', body=body)
        return [Genre(**doc['_source']) for doc in docs['hits']['hits']]

    async def get_genre_list(self) -> list[Genre]:
        genres = await self._get_genre_list_from_elastic()
        return genres or None

    async def _get_genre_list_from_elastic(self) -> list[Genre]:
        docs = await self.elastic.search(index='genres')
        return [Genre(**doc['_source'])for doc in docs['hits']['hits']]


@lru_cache()
def get_genre_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic)
