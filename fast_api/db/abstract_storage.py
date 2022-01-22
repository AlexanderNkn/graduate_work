from abc import ABC, abstractmethod


class AbstractRemoteStorage(ABC):
    """Abstract class for remote storage."""

    @abstractmethod
    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abstractmethod
    async def search(self, *args, **kwargs):
        pass


class AbstractCacheStorage(ABC):
    """Abstract class for cache storage."""

    @abstractmethod
    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abstractmethod
    async def set(self, *args, **kwargs):
        pass
