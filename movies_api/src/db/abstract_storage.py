from abc import ABC, abstractmethod


class AbstractRemoteStorage(ABC):
    """Abstract class for remote storage."""

    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    async def _get_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    async def _get_by_params(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_by_params(self, *args, **kwargs):
        pass


class AbstractCacheStorage(ABC):
    """Abstract class for cache storage."""

    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    async def get_by_key(self, *args, **kwargs):
        pass

    @abstractmethod
    async def set_by_key(self, *args, **kwargs):
        pass

    @abstractmethod
    def create_key(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_obj(self, *args, **kwargs):
        pass

    @abstractmethod
    async def put_obj(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_list(self, *args, **kwargs):
        pass

    @abstractmethod
    async def put_list(self, *args, **kwargs):
        pass
