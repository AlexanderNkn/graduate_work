#!/bin/sh

if [ "$REDIS_DB" = "redis" ]
then
    echo "Waiting for Redis db..."

    while ! nc -z $REDIS_HOST $REDIS_PORT; do
      sleep 0.1
    done

    echo "Redis db started"
fi

if [ "$POSTGRE_NAME" = "movies_database" ]
then
    echo "Waiting for Postgre db..."

    while ! nc -z $POSTGRE_HOST $POSTGRE_PORT; do
      sleep 0.1
    done

    echo "Postgre db started"
fi

exec "$@"
