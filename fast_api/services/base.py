from typing import Union

from db.storage import CacheStorage, RemoteStorage
from models.film import FilmDetailedDTO
from models.genre import GenreDetailedDTO
from models.person import PersonDetailedDTO
from services.utils import get_body

T = Union[FilmDetailedDTO, GenreDetailedDTO, PersonDetailedDTO]


class BaseService:
    def __init__(self, index: str, model: T, storage: RemoteStorage, cache: CacheStorage) -> None:
        self.index = index
        self.model = model
        self.storage = storage
        self.cache = cache

    async def get_by_id(self, id: str) -> T | None:
        cache_key = self.cache.create_key(index=self.index, params=id)
        obj = await self.cache.get_obj(key=cache_key, model=self.model)
        if not obj:
            obj = await self.storage.get_by_id(index=self.index, id=id, model=self.model)
        if obj is not None:
            await self.cache.put_obj(key=cache_key, obj=obj)
            return obj
        return None

    async def get_by_params(self, **params) -> list[T] | None:
        body = get_body(**params)
        cache_key = self.cache.create_key(index=self.index, params=body)
        obj_list = await self.cache.get_list(key=cache_key, model=self.model)
        if not obj_list:
            obj_list = await self.storage.get_by_params(body=body, index=self.index)
        if obj_list is not None:
            await self.cache.put_list(key=cache_key, obj_list=obj_list, model=self.model)
            return obj_list
        return None
