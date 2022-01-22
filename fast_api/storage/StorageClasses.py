from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from storage.AbstractClasses import AbstractCacheStorage, AbstractRemoteStorage


class ElasticStorage(AbstractRemoteStorage):

    def __init__(self, engine: AsyncElasticsearch):
        self.engine = engine

    async def get(self, *args, **kwargs):
        return await self.engine.get(*args, **kwargs)
    
    async def search(self, *args, **kwargs):
        return await self.engine.search(*args, **kwargs)


class RedisCacheStorage(AbstractCacheStorage):

    def __init__(self, engine: Redis):
        self.engine = engine
    
    async def get(self, *args, **kwargs):
        return await self.engine.get(*args, **kwargs)
    
    async def set(self, *args, **kwargs):
        return await self.engine.set(*args, **kwargs)
