#!/bin/bash

#echo "Running Mongo tests..."
#pytest api/tests/mongo_tests/* -s -o DJANGO_SETTINGS_MODULE=rest.mongodb_test_settings -o addopts=--cov=api/views --cov-report  html --reuse-db
echo "Running Postgres tests..."
pytest api/tests/postgresql_tests/* -s -o DJANGO_SETTINGS_MODULE=rest.postgres_test_settings -o addopts=--cov=api/views --cov-report  html --reuse-db
