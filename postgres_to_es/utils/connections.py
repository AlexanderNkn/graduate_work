import os
from os.path import dirname, join
from typing import Optional

import psycopg2
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from psycopg2.extensions import connection as PGconnection

from .backoff import backoff

dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)


class ElasticConnection:
    """Provides method for automatic reconnection to Elastic db."""
    def __init__(self) -> None:
        self.socket = {'host': os.getenv('ES_HOST'), 'port': os.getenv('ES_PORT')}
        self._client = Elasticsearch([self.socket])

    @backoff(initial_backoff=1, max_backoff=60)
    def get_client(self) -> Optional[Elasticsearch]:
        return self._client if self._client.ping() else None


class PostgresConnection:
    """Provides method for automatic reconnection to Postgres db."""
    def __init__(self) -> None:
        self.dsn = {
            'dbname': os.getenv('PG_DBNAME'),
            'user': os.getenv('PG_USER'),
            'password': os.getenv('PG_PASSWORD'),
            'host': os.getenv('PG_HOST'),
            'port': os.getenv('PG_PORT'),
            'options': os.getenv('PG_OPTIONS'),
        }

    @backoff(initial_backoff=1, max_backoff=60)
    def get_connection(self) -> Optional[PGconnection]:
        try:
            return psycopg2.connect(**self.dsn)
        except psycopg2.OperationalError:
            return None
