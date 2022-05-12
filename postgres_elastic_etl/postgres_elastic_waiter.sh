#!/bin/sh

if [ "$PG_DBNAME" = "movies_database" ]
then
    echo "Waiting for Postgres db ..."

    while ! nc -z $PG_HOST $PG_PORT; do
      sleep 5
    done

    echo "Postgres db started"
fi

if [ "$ES_HOST" = "es" ]
then
    echo "Waiting for ElasticSearch ..."

    while ! nc -z $ES_HOST $ES_PORT; do
      sleep 5
    done

    echo "ElasticSearch db started"
fi

exec "$@"