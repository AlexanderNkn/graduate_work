from aioredis import Redis

from db.abstract_storage import AbstractCacheStorage

redis: Redis | None = None


async def get_redis() -> Redis:
    return redis


class RedisCacheStorage(AbstractCacheStorage):

    def __init__(self, engine: Redis):
        self.engine = engine

    async def get(self, *args, **kwargs):
        return await self.engine.get(*args, **kwargs)

    async def set(self, *args, **kwargs):
        return await self.engine.set(*args, **kwargs)
