from elasticsearch import AsyncElasticsearch

from db.abstract_storage import AbstractRemoteStorage

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch | None:
    return es


class ElasticStorage(AbstractRemoteStorage):

    def __init__(self, engine: AsyncElasticsearch):
        self.engine = engine

    async def get(self, *args, **kwargs):
        return await self.engine.get(*args, **kwargs)

    async def search(self, *args, **kwargs):
        return await self.engine.search(*args, **kwargs)
