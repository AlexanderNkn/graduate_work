from redis import Redis

redis: Redis | None = None


def jwt_redis_blocklist() -> Redis:
    return redis
