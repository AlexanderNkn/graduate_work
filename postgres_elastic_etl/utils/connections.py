import os
from typing import Optional

import psycopg2
from elasticsearch import Elasticsearch, ConnectionError as ES_ConnectionError
from psycopg2.extensions import connection as PGconnection  # noqa: N812

from .backoff import backoff


class ElasticConnection:
    """Provides method for automatic reconnection to Elastic db."""

    def __init__(self) -> None:
        self.socket = {'host': os.getenv('ES_HOST'), 'port': os.getenv('ES_PORT')}
        self._client = Elasticsearch([self.socket])

    @backoff(exception=ES_ConnectionError, initial_backoff=1, max_backoff=60, max_retries=1000)
    def get_client(self) -> Optional[Elasticsearch]:
        if not self._client.ping():
            raise ES_ConnectionError
        return self._client


class PostgresConnection:
    """Provides method for automatic reconnection to Postgres db."""

    def __init__(self) -> None:
        self.dsn = {
            'dbname': os.getenv('PG_DBNAME'),
            'user': os.getenv('PG_USER'),
            'password': os.getenv('PG_PASSWORD'),
            'host': os.getenv('PG_HOST'),
            'port': int(os.getenv('PG_PORT')),
            'options': os.getenv('PG_OPTIONS'),
        }

    def get_connection(self) -> Optional[PGconnection]:
        return psycopg2.connect(**self.dsn)
