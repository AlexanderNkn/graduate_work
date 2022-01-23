from aioredis import Redis

redis: Redis | None = None


async def get_redis() -> Redis:
    return redis


class RedisStorage:

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_by_key(self, key, *args, **kwargs):
        return await self.redis.get(key, *args, **kwargs)

    async def set_by_key(self, key, value, *args, **kwargs):
        return await self.redis.set(key, value, *args, **kwargs)
