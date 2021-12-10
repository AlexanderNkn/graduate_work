"""Module provides methods for sequential data transfer from Postgres to Elasticsearch.

Number of records in batch could be set up in TRANSFER_BATCH_SIZE. Certain number of records,
according batch size, will be fetched from Postgres and immediately upload to Elasticsearch.
Then the process will be repeated untill all data from Postgres would be transfered to Elasticsearch.
"""
import json
import logging
import os
from logging import config
from os.path import dirname, join
from time import sleep
from typing import Any, Generator

import elasticsearch
import psycopg2
from elasticsearch.helpers import bulk

from sql import SQL
from utils.connections import ElasticConnection, PostgresConnection
from utils.etl_state import JsonFileStorage, State
from utils.logging_config import LOGGING_CONFIG

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('main')

TRANSFER_BATCH_SIZE = 100
# path for ElasticSearch index schema
SCHEMA_PATH = join(dirname(__file__), 'es_schema.json')
# path for ETL latest state
STATE_PATH = join(dirname(__file__), 'etl_state.json')


class ETL:
    """Extracts data from Postges then load it to ElasticSearch."""

    def extract(self) -> Generator[list[tuple], None, None]:
        """Retrieve data from Postgres.
        Keeps state of the last call to continue retrieving data starting from
        the save point.
        """
        while True:
            storage = JsonFileStorage(STATE_PATH)
            state = State(storage)
            latest_update: str = state.get_state(key='latest_update')

            logger.info('Getting connection with Postgres db ...')
            pg_connection = PostgresConnection()
            conn = pg_connection.get_connection()
            logger.info('Connection with Postgres was successfully established')
            with conn.cursor() as cur:
                try:
                    # With provided sql script all updated data for film_works,
                    # persons and genres are selected in one query
                    cur.execute(SQL, (latest_update, latest_update, latest_update))
                except (psycopg2.OperationalError, psycopg2.errors.AdminShutdown):
                    logger.error('Lost connection with Postgres. Try to reconnect.')
                    continue
                except Exception:
                    logger.exception('Postgres db crashed ')
                    break
                else:
                    logger.info('Uploading data from Postgres to Elastic started')
                    while True:
                        batch: list[tuple] = cur.fetchmany(TRANSFER_BATCH_SIZE)
                        if not batch:
                            break
                        yield batch
                        latest_update = batch[-1][-1].strftime('%Y-%m-%d %H:%M:%S.%f')
                        state.set_state(key='latest_update', value=latest_update)
                        logger.info('Batch successfully uploaded, ETL state was updated')
                    break

    def transform(self, data: Generator[list[tuple], None, None]) -> Generator[dict[str, Any], None, None]:
        """Transforms raw data to required by ElasticSearch format."""
        for row in data:
            for id, rating, title, description, persons, genres, _ in row:
                genre = ' '.join({item['genre'] for item in genres if item.get('genre')})
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
                    'director': directors_names and directors_names[0] or None,
                    'actors_names': actors_names and [' '.join(actors_names)] or None,
                    'writers_names': writers_names and [' '.join(writers_names)] or None,
                    'actors': actors,
                    'writers': writers,
                }
                yield doc

    def load(self, data: Generator[dict[str, Any], None, None]) -> None:
        """Load data to Elasticsearch.
        Keeps state of the last call to continue loading data starting from
        the save point.
        """
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
                    actions=data,
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
                break

    def create_index(self, client):
        """Creates an index in Elasticsearch if one isn't already there."""
        with open(SCHEMA_PATH, 'r') as schema:
            client.indices.create(
                index='movies',
                body=json.load(schema),
                ignore=400,
            )

    def run(self) -> None:
        """Runs ETL processes."""
        raw_data = self.extract()
        prepared_data = self.transform(raw_data)
        self.load(prepared_data)


if __name__ == '__main__':
    etl_process = ETL()
    while True:
        try:
            etl_process.run()
            sleep(float(os.getenv('UPLOAD_INTERVAL')))
        except Exception:
            logger.exception('Main process failed: ')
