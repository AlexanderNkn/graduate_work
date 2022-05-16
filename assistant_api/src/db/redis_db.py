import aioredis.errors  # noqa: WPS301
import backoff
from aioredis import Redis

from core.config import settings

redis: Redis | None = None


async def get_redis() -> Redis:
    return redis
