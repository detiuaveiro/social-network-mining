#!/bin/bash

echo "Running Mongo tests..."
python -m pytest api/tests/mongo_tests/* -x -o DJANGO_SETTINGS_MODULE=rest.mongodb_test_settings
echo "Running Postgres tests..."
python -m pytest api/tests/postgresql_tests/* -x -o DJANGO_SETTINGS_MODULE=rest.postgres_test_settings
echo "Running Neo4j tests..."
python -m pytest api/tests/neo4j_tests/* -x -o DJANGO_SETTINGS_MODULE=rest.settings
