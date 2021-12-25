from typing import Union

from elasticsearch import AsyncElasticsearch
import elasticsearch.exceptions

from models.film import Film
from models.genre import Genre
from models.person import Person

from .utils import get_body

T = Union[Film, Genre, Person]


class BaseService:
    def __init__(self, index: str, model: T, elastic: AsyncElasticsearch) -> None:
        self.index = index
        self.model = model
        self.elastic = elastic

    async def get_by_id(self, id: str) -> T:
        try:
            doc = await self.elastic.get(index=self.index, id=id)
            obj = self.model(**doc['_source'])
        except elasticsearch.exceptions.NotFoundError:
            obj = None
        return obj

    async def get_by_params(self, **params) -> list[T]:
        body = get_body(**params)
        try:
            doc = await self.elastic.search(body=body, index=self.index)
            obj_list = [self.model(**_doc['_source']) for _doc in doc['hits']['hits']]
        except elasticsearch.exceptions.NotFoundError:
            obj_list = None
        return obj_list
