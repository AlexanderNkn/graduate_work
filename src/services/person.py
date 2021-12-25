from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from models.person import Person

from .base import BaseService


class PersonService(BaseService):
    pass


@lru_cache()
def get_person_service(elastic: AsyncElasticsearch = Depends(get_elastic),) -> PersonService:
    return PersonService(index='persons', model=Person, elastic=elastic)
