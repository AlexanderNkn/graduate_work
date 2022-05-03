from typing import Union

from orjson import loads as orjson_loads

from core import config
from db.abstract_storage import AbstractCacheStorage, AbstractRemoteStorage
from models.base import orjson_dumps
from models.film import FilmDetailedDTO
from models.genre import GenreDetailedDTO
from models.person import PersonDetailedDTO

T = Union[FilmDetailedDTO, GenreDetailedDTO, PersonDetailedDTO]


class RemoteStorage(AbstractRemoteStorage):

    async def _get_by_id(self, index, id, *args, **kwargs):
        return await self.engine.get_by_id(index=index, id=id, *args, **kwargs)

    async def _get_by_params(self, index, body, *args, **kwargs):
        return await self.engine.get_by_params(index=index, body=body, *args, **kwargs)

    async def get_by_id(self, index: str, id: str, model: T, *args, **kwargs) -> T | None:
        doc = await self._get_by_id(index=index, id=id, *args, **kwargs)
        if doc is not None:
            return model(**doc['_source'])
        return None

    async def get_by_params(self, index: str, body: dict, model: T, *args, **kwargs) -> list[T] | None:
        doc = await self._get_by_params(index=index, body=body, *args, **kwargs)
        if doc is not None:
            return [model(**_doc['_source']) for _doc in doc['hits']['hits']]
        return None


class CacheStorage(AbstractCacheStorage):

    async def get_by_key(self, key, *args, **kwargs):
        return await self.engine.get_by_key(key=key, *args, **kwargs)

    async def set_by_key(self, key, value, *args, **kwargs):
        return await self.engine.set_by_key(key=key, value=value, *args, **kwargs)

    def create_key(self, index: str, params: str | dict):
        return index + str(hash(orjson_dumps(params)))

    async def get_obj(self, key: str, model: T) -> T | None:
        data = await self.get_by_key(key)
        if not data:
            return None
        return model.parse_raw(data)

    async def put_obj(self, key: str, obj: T) -> None:
        await self.set_by_key(key=key, value=obj.json(), expire=config.CACHE_EXPIRE_IN_SECONDS)

    async def get_list(self, key: str, model: T) -> list[T] | None:
        data = await self.get_by_key(key)
        if not data:
            return None
        return [model.parse_raw(doc) for doc in orjson_loads(data)]

    async def put_list(self, key: str, obj_list: list[T], model: T) -> None:
        await self.set_by_key(
            key=key, value=orjson_dumps(obj_list, default=model.json), expire=config.CACHE_EXPIRE_IN_SECONDS
        )
