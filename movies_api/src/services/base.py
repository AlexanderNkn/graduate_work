from typing import Union

from db.storage import CacheStorage, RemoteStorage
from models.film import FilmDetailedDTO
from models.genre import GenreDetailedDTO
from models.person import PersonDetailedDTO
from services.utils import get_body

T = Union[FilmDetailedDTO, GenreDetailedDTO, PersonDetailedDTO]  # noqa: WPS111

# attrs that have to be implemented in BaseService and all child classes
MANDATORY_ATTRS = ('index', 'model')


class BaseServiceAttrs(type):
    """Checks for mandatory attrs in child classes."""

    mandatory_attrs = MANDATORY_ATTRS

    def __new__(mcls, name, bases, mdct):
        cls = super().__new__(mcls, name, bases, mdct)
        for attr in mcls.mandatory_attrs:
            if attr not in mdct:
                raise AttributeError(f'Class attribute `{attr}` is mandatory for class {name}')
        return cls


class BaseService(metaclass=BaseServiceAttrs):
    index: str | None = None
    model: T | None = None

    def __init__(self, storage: RemoteStorage, cache: CacheStorage) -> None:
        self.storage = storage
        self.cache = cache

    async def get_by_id(self, id: str) -> T | None:
        cache_key = self.cache.create_key(index=self.index, params=id)
        if obj := await self.cache.get_obj(key=cache_key, model=self.model):
            return obj
        if obj := await self.storage.get_by_id(index=self.index, id=id, model=self.model):
            await self.cache.put_obj(key=cache_key, obj=obj)
            return obj
        return None

    async def get_by_params(self, **params) -> list[T] | None:
        body = get_body(**params)
        cache_key = self.cache.create_key(index=self.index, params=body)
        if obj_list := await self.cache.get_list(key=cache_key, model=self.model):
            return obj_list
        if obj_list := await self.storage.get_by_params(body=body, index=self.index, model=self.model):
            await self.cache.put_list(key=cache_key, obj_list=obj_list, model=self.model)
            return obj_list
        return None
