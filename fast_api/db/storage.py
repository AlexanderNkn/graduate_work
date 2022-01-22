from .elastic_db import ElasticStorage
from .redis_db import RedisCacheStorage


class RemoteStorage(ElasticStorage):
    pass


class CacheStorage(RedisCacheStorage):
    pass
