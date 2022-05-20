#!/bin/bash

# prepare .env files
cp movies_admin/envs/.admin.env.sample movies_admin/envs/.admin.env

cp postgres/envs/.movies_admin_db.env.sample postgres/envs/.movies_admin_db.env
cp postgres/envs/.auth_db.env.sample postgres/envs/.auth_db.env
cp postgres_elastic_etl/envs/.etl.env.sample postgres_elastic_etl/envs/.etl.env

cp auth/envs/.auth.env.sample auth/envs/.auth.env
cp movies_api/envs/.movies_api.env.sample movies_api/envs/.movies_api.env

# prepare state file for etl
cp postgres_elastic_etl/data/etl_state_sample.json postgres_elastic_etl/data/etl_state.json

# build images
docker-compose build
docker-compose -f docker-compose.yml -f docker-compose.initial.yml up -d movies_admin_db es auth

# add schema to movies db
echo "Waiting for movies db..."
ping -c 1 127.0.0.1 5433 &> /dev/null
echo "Movies db started"

export PGPASSWORD=1234
psql -U postgres -h localhost -p 5433 -f movies_admin/data/demo_with_image_fields.sql -d movies_database

# add user to auth db
echo "Waiting for auth db..."
ping -c 1 127.0.0.1 5434 &> /dev/null
echo "Auth db started"

psql -U postgres -h localhost -p 5434 -c "create role auth with login password '1234';"
# drop previous db because of alembic conflict
psql -U postgres -h localhost -p 5434 -c "drop database if exists auth_database;"
psql -U postgres -h localhost -p 5434 -c "drop database if exists auth_database_test;"
psql -U postgres -h localhost -p 5434 -c "create database auth_database;"
psql -U postgres -h localhost -p 5434 -c "create database auth_database_test;"
psql -U postgres -h localhost -p 5434 -c "grant all privileges on database auth_database to auth;"
psql -U postgres -h localhost -p 5434 -c "grant all privileges on database auth_database_test to auth;"

# add schema to elastic
curl --connect-timeout 60 \
     --max-time 120 \
     --retry 10 \
     --retry-delay 0 \
     --retry-max-time 80 \
     --retry-connrefused \
    -X PUT -H "Content-Type: application/json" --data @postgres_elastic_etl/data/movies_index.json -k http://localhost:9201/movies -w "\n"
curl -X PUT -H "Content-Type: application/json" --data @postgres_elastic_etl/data/persons_index.json -k http://localhost:9201/persons -w "\n"
curl -X PUT -H "Content-Type: application/json" --data @postgres_elastic_etl/data/genres_index.json -k http://localhost:9201/genres -w "\n"
curl -X GET http://localhost:9201/_cat/indices

# remove containers
docker-compose down
