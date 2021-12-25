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
        except elasticsearch.exceptions.NotFoundError:
            obj = None
        else:
            obj = self.model(**doc['_source'])
        return obj

    async def get_by_params(self, **params) -> list[T]:
        body = get_body(**params)
        try:
            doc = await self.elastic.search(body=body, index=self.index)
        except elasticsearch.exceptions.NotFoundError:
            obj_list = None
        else:
            obj_list = [self.model(**_doc['_source']) for _doc in doc['hits']['hits']]
        return obj_list
