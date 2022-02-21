#!/bin/sh

if [ "$REDIS_DB_TEST" = "redis" ]
then
    echo "Waiting for Redis db..."

    while ! nc -z $REDIS_HOST_TEST $REDIS_PORT_TEST; do
      sleep 0.1
    done

    echo "Redis db started"
fi

if [ "$ELASTIC_DB_TEST" = "elastic" ]
then
    echo "Waiting for Elasticsearch db..."

    while ! nc -z $ELASTIC_HOST_TEST $ELASTIC_PORT_TEST; do
      sleep 0.1
    done

    echo "Elasticsearch db started"
fi

exec "$@"
