import aioredis.errors  # noqa: WPS301
import backoff
from aioredis import Redis
from fastapi import Depends

from core.config import settings
from dependencies.authentication import get_user_identity

redis: Redis | None = None


class RedisStorage:

    def __init__(self, redis: Redis, key: str):  # noqa: WPS442
        self.redis = redis
        self.key = key

    @backoff.on_exception(backoff.expo, aioredis.errors.RedisError, max_time=10)
    async def get(self, *args, **kwargs):
        return await self.redis.get(key=self.key, *args, **kwargs)

    @backoff.on_exception(backoff.expo, aioredis.errors.RedisError, max_time=10)
    async def set(self, value, *args, **kwargs):
        return await self.redis.set(key=self.key, value=value, expire=settings.cache_expire, *args, **kwargs)


async def get_redis(key: str = Depends(get_user_identity)) -> RedisStorage:
    return RedisStorage(redis, key)
