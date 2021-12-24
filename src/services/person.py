from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from models.person import Person

from .utils import get_body


class PersonService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        doc = await self.elastic.get(index='persons', id=person_id)
        person = Person(**doc['_source'])
        return person or None

    async def get_persons_by_params(self, **params) -> Optional[list[Person]]:
        body = get_body(**params)
        docs = await self.elastic.search(index='persons', body=body)
        person_list = [Person(**doc['_source']) for doc in docs['hits']['hits']]
        return person_list


@lru_cache()
def get_person_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(elastic)
