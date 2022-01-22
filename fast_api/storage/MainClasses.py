from storage.StorageClasses import ElasticStorage, RedisCacheStorage


class RemoteStorage(ElasticStorage):
    pass


class CacheStorage(RedisCacheStorage):
    pass
