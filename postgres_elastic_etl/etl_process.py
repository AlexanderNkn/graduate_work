"""Module provides methods for sequential data transfer from Postgres to Elasticsearch.

Number of records in batch could be set up in TRANSFER_BATCH_SIZE. Certain number of records,
according batch size, will be fetched from Postgres and immediately upload to Elasticsearch.
Then the process will be repeated untill all data from Postgres would be transfered to Elasticsearch.
"""
import logging
import os
from datetime import datetime
import signal
import sys
from logging import config
from os.path import dirname, join
from time import sleep
from typing import Any, Optional

import elasticsearch
from elasticsearch.client import Elasticsearch
import psycopg2
from elasticsearch.helpers import bulk, BulkIndexError

from sql import get_sql_query
from es_schema import GENRES_INDEX, MOVIES_INDEX, PERSONS_INDEX
from utils.backoff import backoff
from utils.connections import ElasticConnection, PostgresConnection
from utils.etl_state import JsonFileStorage, State
from utils.logging_config import LOGGING_CONFIG

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('main')

# number of rows that are fetch from Postgres then upload to Elastic in one iteration
TRANSFER_BATCH_SIZE = 500
# path for ETL latest state
STATE_PATH = join(dirname(__file__), 'data/etl_state.json')


class ExtractData:

    def __init__(self) -> None:
        self.connection = PostgresConnection()
        self.state = State(JsonFileStorage(STATE_PATH))
    
    @backoff(
        exception=(psycopg2.OperationalError, psycopg2.errors.AdminShutdown),
        initial_backoff=1,
        max_backoff=60,
        max_retries=10,
        msg='Lost connection with Postgres.',
    )
    def _fetch_data(self, index: str, updated_at: str):
        logger.info('Getting connection with Postgres db ...')
        pg_connection = self.connection.get_connection()
        logger.info('Connection with Postgres was successfully established')
        with pg_connection.cursor() as cursor:
            cursor.execute(*get_sql_query(index, updated_at=updated_at, batch_size=TRANSFER_BATCH_SIZE))
            data = cursor.fetchall()
            message = (f'Uploading {index} data from Postgres to Elastic started' if data
                       else f'No updates available for {index}')
            logger.info(message)
            return data
  
    def extract(self, index: str) -> Optional[list[tuple]]:
        """Retrieve data from Postgres.
        Keeps state of the last call to continue retrieving data starting from
        the save point.
        """
        logger.info(f'Searching for {index} updates in Postgres db')
        latest_update: str = self.state.get_state(key=f'{index}_latest_update')
        try:
            return self._fetch_data(index, latest_update)
        except Exception:
            logger.error('Postgres db crashed ')
            raise


class TransformData:
    def transform(self, data: list[tuple], index: str) -> dict[str, list[dict[str, Any]] | datetime]:
        """Transforms raw data to required by ElasticSearch format."""
        prepared_data, updated_at = {
            'movies': self.prepare_movies_data,
            'genres': self.prepare_genres_data,
            'persons': self.prepare_persons_data,
        }[index](data)

        return {
            'prepared_data': prepared_data,  # type: ignore
            'latest_update': updated_at,  # type: ignore
        }

    def prepare_movies_data(self, data: list[tuple]) -> tuple[list[dict[str, Any]], datetime]:
        prepared_data = []
        for id, rating, title, description, persons, genres, latest_update in data:
            genres = list({genre['id']: genre for genre in genres}.values())
            actors_names, actors, writers_names, writers, directors_names, directors = [], [], [], [], [], []
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
                    directors.append(person_info)

            doc = {
                '_id': id,
                'id': id,
                'imdb_rating': rating,
                'genre': genres,
                'title': title,
                'description': description or None,
                'directors_names': directors_names or None,
                'actors_names': actors_names or None,
                'writers_names': writers_names or None,
                'directors': directors,
                'actors': actors,
                'writers': writers,
            }
            prepared_data.append(doc)

        return prepared_data, latest_update

    def prepare_genres_data(self, data: list[tuple]) -> tuple[list[dict[str, Any]], datetime]:
        prepared_data = []
        for id, name, description, latest_update in data:
            doc = {
                '_id': id,
                'id': id,
                'name': name,
                'description': description or None,
            }
            prepared_data.append(doc)

        return prepared_data, latest_update

    def prepare_persons_data(self, data: list[tuple]) -> tuple[list[dict[str, Any]], datetime]:
        prepared_data = []
        for id, full_name, role, film_ids, latest_update in data:
            doc = {
                '_id': id,
                'id': id,
                'full_name': full_name,
                'role': role,
                'film_ids': film_ids,
            }
            prepared_data.append(doc)

        return prepared_data, latest_update


class LoadData:
    INDEXES = {
        'movies': MOVIES_INDEX,
        'genres': GENRES_INDEX,
        'persons': PERSONS_INDEX,
    }

    def __init__(self) -> None:
        self.connection = ElasticConnection()
        self.state = State(JsonFileStorage(STATE_PATH))

    def create_index(self, client: Elasticsearch, index: str):
        """Creates an index in Elasticsearch if one isn't already there."""
        client.indices.create(
            index=index,
            ignore=400,
            **self.INDEXES[index],
        )

    @backoff(
        exception=elasticsearch.ConnectionError,
        initial_backoff=1,
        max_backoff=60,
        max_retries=10,
        msg='Lost connection with Elastic.',
    )
    def _load_data(self, index: str, data: list[dict[str, Any]]):
        logger.info('Getting connection with Elastic db ...')
        client = self.connection.get_client()
        logger.info('Connection with Elastic was successfully established')
        self.create_index(client, index)
        success, _ = bulk(
            client=client,
            index=index,
            actions=data,
            chunk_size=TRANSFER_BATCH_SIZE,
            max_retries=100,
            initial_backoff=1,
            max_backoff=300,
        )
        return success


    def load(self, data: dict[str, Any], statistics: dict[str, int], index: str) -> None:
        """Load data to Elasticsearch.
        Keeps state of the last call to continue loading data starting from
        the save point.
        """
        try:
            success = self._load_data(index, data['prepared_data'])
        except BulkIndexError as exp:
            logger.error(f'Elastic db crashed \n{exp.errors[0]}')
        else:
            logger.info(f'Batch {statistics["batch_number"]} was uploaded successfully from Postgres to Elastic')
            statistics['batch_number'] += 1
            statistics['total'] += success
            latest_update = data['latest_update'].strftime('%Y-%m-%d %H:%M:%S.%f')
            self.state.set_state(key=f'{index}_latest_update', value=latest_update)
            logger.info('ETL state was updated')


class Process:
    """Extracts data from Postges then load it to ElasticSearch."""
    def __init__(self) -> None:
        self.extractdata = ExtractData()
        self.transformdata = TransformData()
        self.loaddata = LoadData()

    def run(self) -> None:
        """Runs ETL processes."""
        for index in self.loaddata.INDEXES:
            statistics = {
                'batch_number': 1,
                'total': 0,
            }
            while True:
                raw_data = self.extractdata.extract(index)
                if not raw_data:
                    break
                prepared_data = self.transformdata.transform(raw_data, index)
                self.loaddata.load(prepared_data, statistics, index)
            logger.info(f'Uploading {index} data from Postgres to Elastic completed - '
                        f'{statistics["total"]} rows were synchronized')


if __name__ == '__main__':
    etl_process = Process()

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
