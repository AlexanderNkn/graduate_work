"""Module provides methods for sequential data transfer from Postgres to Elasticsearch.

Number of records in batch could be set up in TRANSFER_BATCH_SIZE. Certain number of records,
according batch size, will be fetched from Postgres and immediately upload to Elasticsearch.
Then the process will be repeated untill all data from Postgres would be transfered to Elasticsearch.
"""
import json
from os.path import dirname, join
from typing import Any, Generator

import elasticsearch
import psycopg2
from elasticsearch.helpers import bulk

from utils.connections import ElasticConnection, PostgresConnection
from utils.etl_state import JsonFileStorage, State

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
            pg_connection = PostgresConnection()
            conn = pg_connection.get_connection()
            with conn.cursor() as cur:
                sql = """
                    SELECT
                        fw.id, fw.rating, fw.title, fw.description,
                        jsonb_agg(jsonb_build_object('id', p.id, 'full_name', p.full_name, 'role', pfw.role)) AS persons,
                        jsonb_agg(jsonb_build_object('id', g.id, 'genre', g.name)) AS genres,
                        GREATEST(fw.updated_at, MAX(p.updated_at), MAX(g.updated_at)) AS latest_update
                    FROM content.film_work fw
                    LEFT OUTER JOIN content.person_film_work pfw ON fw.id = pfw.film_work_id
                    LEFT OUTER JOIN content.person p ON p.id = pfw.person_id
                    LEFT OUTER JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
                    LEFT OUTER JOIN content.genre g ON gfw.genre_id = g.id
                    WHERE fw.updated_at > %s or p.updated_at > %s or g.updated_at > %s
                    GROUP BY fw.id
                    ORDER BY latest_update;
                """
                try:
                    cur.execute(sql, (latest_update, latest_update, latest_update))
                except (psycopg2.OperationalError, psycopg2.errors.AdminShutdown):
                    continue
                except Exception:
                    break
                else:
                    while True:
                        batch: list[tuple] = cur.fetchmany(TRANSFER_BATCH_SIZE)
                        if not batch:
                            break
                        yield batch
                        latest_update = batch[-1][-1].strftime('%Y-%m-%d %H:%M:%S.%f')
                        state.set_state(key='latest_update', value=latest_update)
                    break

    def transform(self, data: Generator[list[tuple], None, None]) -> Generator[dict[str, Any], None, None]:
        """Transforms raw data to required by ElasticSearch format."""
        for row in data:
            for id, rating, title, description, persons, genres, _ in [*row]:
                genre = ' '.join({item['genre'] for item in genres if item.get('genre')})
                actors_names, actors, writers_names, writers, directors_names = [], [], [], [], []
                unique_persons = list({person['id']: person for person in persons}.values())
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
            es_connection = ElasticConnection()
            client = es_connection.get_client()
            try:
                self.create_index(client)
                bulk(
                    client=client,
                    index='movies',
                    actions=data,
                    chunk_size=TRANSFER_BATCH_SIZE,
                    max_retries=1000,
                    initial_backoff=1,
                    max_backoff=300,
                )
            except elasticsearch.ConnectionError:
                continue
            except Exception:
                break
            else:
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
    etl_process.run()
