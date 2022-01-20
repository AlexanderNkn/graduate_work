from abc import ABC, abstractmethod


class AbstractRemoteStorage(ABC):
    """Абстрактный класс для работы с Remote хранилищем"""

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
    """Абстрактный класс для работы с Cache хранилещем"""

    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abstractmethod
    async def set(self, *args, **kwargs):
        pass
