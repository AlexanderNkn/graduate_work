"""Module provides methods for sequential data transfer from Postgres to Elasticsearch.

Number of records in batch could be set up in TRANSFER_BATCH_SIZE. Certain number of records,
according batch size, will be fetched from Postgres and immediately upload to Elasticsearch.
Then the process will be repeated untill all data from Postgres would be transfered to Elasticsearch.
"""
import json
import logging
import os
from datetime import datetime
import signal
import sys
from logging import config
from os.path import dirname, join
from time import sleep
from typing import Any, Optional, Sequence

import elasticsearch
import psycopg2
from elasticsearch.helpers import bulk

from sql import SQL_FOR_UPDATE_FILMWORK_INDEX
from utils.connections import ElasticConnection, PostgresConnection
from utils.etl_state import JsonFileStorage, State
from utils.logging_config import LOGGING_CONFIG

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('main')

TRANSFER_BATCH_SIZE = 500
# path for ElasticSearch index schema
SCHEMA_PATH = join(dirname(__file__), 'es_schema.json')
# path for ETL latest state
STATE_PATH = join(dirname(__file__), 'data/etl_state.json')


class ETL:
    """Extracts data from Postges then load it to ElasticSearch."""

    def extract(self) -> Optional[list[tuple]]:
        """Retrieve data from Postgres.
        Keeps state of the last call to continue retrieving data starting from
        the save point.
        """
        logger.info('Searching for updates in Postgres db')
        state = self.get_state_object()
        latest_update: str = state.get_state(key='latest_update')

        while True:
            logger.info('Getting connection with Postgres db ...')
            pg_connection = PostgresConnection()
            conn = pg_connection.get_connection()
            logger.info('Connection with Postgres was successfully established')
            with conn.cursor() as cur:
                try:
                    # With provided sql script all updated data for film_works,
                    # persons and genres are selected in one query
                    cur.execute(
                        SQL_FOR_UPDATE_FILMWORK_INDEX,
                        (latest_update, latest_update, latest_update, TRANSFER_BATCH_SIZE)
                    )
                except (psycopg2.OperationalError, psycopg2.errors.AdminShutdown):
                    logger.error('Lost connection with Postgres. Try to reconnect.')
                    continue
                except Exception:
                    logger.exception('Postgres db crashed ')
                    break
                else:
                    data = cur.fetchall()
                    message = 'Uploading data from Postgres to Elastic started' if data else 'No updates available'
                    logger.info(message)
                    return data

        return None

    def transform(self, data: list[tuple]) -> dict[str, Sequence[Any] | datetime]:
        """Transforms raw data to required by ElasticSearch format."""
        prepared_data = []
        for id, rating, title, description, persons, genres, latest_update in data:
            genre = [*{item['genre'] for item in genres if item.get('genre')}]
            actors_names, actors, writers_names, writers, directors_names = [], [], [], [], []
            unique_persons = ({person['id']: person for person in persons}.values())
            for person in unique_persons:
                if not person.get('role'):
                    continue
                person_info = {'id': person['id'], 'name': person['full_name']}
                if person['role'] == 'actor':
                    actors_names.append(person['full_name'])
                    actors.append(person_info)
                elif person['role'] == 'writer':
                    writers_names.append(person['full_name'])
                    writers.append(person_info)
                elif person['role'] == 'director':
                    directors_names.append(person['full_name'])

            doc = {
                '_id': id,
                'id': id,
                'imdb_rating': rating,
                'genre': genre,
                'title': title,
                'description': description,
                'director': directors_names or None,
                'actors_names': actors_names or None,
                'writers_names': writers_names or None,
                'actors': actors,
                'writers': writers,
            }
            prepared_data.append(doc)

        return {
            'prepared_data': prepared_data,
            'latest_update': latest_update
        }

    def load(self, data: dict[str, Any]) -> None:
        """Load data to Elasticsearch.
        Keeps state of the last call to continue loading data starting from
        the save point.
        """
        state = self.get_state_object()
        while True:
            logger.info('Getting connection with Elastic db ...')
            es_connection = ElasticConnection()
            client = es_connection.get_client()
            logger.info('Connection with Elastic was successfully established')
            try:
                self.create_index(client)
                success, _ = bulk(
                    client=client,
                    index='movies',
                    actions=data['prepared_data'],
                    chunk_size=TRANSFER_BATCH_SIZE,
                    max_retries=1000,
                    initial_backoff=1,
                    max_backoff=300,
                )
            except elasticsearch.ConnectionError:
                logger.error('Lost connection with Elastic. Try to reconnect.')
                continue
            except Exception:
                logger.exception('Elastic db crashed ')
                break
            else:
                logger.info('Uploading data from Postgres to Elastic completed - '
                            f'{success} rows were synchronized')
                latest_update = data['latest_update'].strftime('%Y-%m-%d %H:%M:%S.%f')
                state.set_state(key='latest_update', value=latest_update)
                logger.info('ETL state was updated')
                break

    def create_index(self, client):
        """Creates an index in Elasticsearch if one isn't already there."""
        with open(SCHEMA_PATH, 'r') as schema:
            client.indices.create(
                index='movies',
                body=json.load(schema),
                ignore=400,
            )

    def get_state_object(self) -> State:
        """Returns state instance."""
        storage = JsonFileStorage(STATE_PATH)
        return State(storage)

    def run(self) -> None:
        """Runs ETL processes."""
        while True:
            raw_data = self.extract()
            if not raw_data:
                break
            prepared_data = self.transform(raw_data)
            self.load(prepared_data)


if __name__ == '__main__':
    etl_process = ETL()

    def handler_stop_signals(signum, frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, handler_stop_signals)
    signal.signal(signal.SIGTERM, handler_stop_signals)

    while True:
        try:
            etl_process.run()
        except Exception:
            logger.exception('Main process failed: ')
        sleep(float(os.getenv('UPLOAD_INTERVAL')))  # type: ignore
