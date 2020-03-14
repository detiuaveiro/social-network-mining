#!/bin/bash

echo "Running Mongo tests..."
pytest api/tests/mongo_tests/* -o DJANGO_SETTINGS_MODULE=rest.mongodb_test_settings -o addopts=--cov=api/views --cov-report  html --reuse-db
echo "Running Postgres tests..."
pytest api/tests/postgresql_tests/*  -o DJANGO_SETTINGS_MODULE=rest.postgres_test_settings -o addopts=--cov=api/views --cov-report  html --reuse-db
echo "Running Neo4j tests..."
pytest api/tests/neo4j_tests/*  -o DJANGO_SETTINGS_MODULE=rest.settings -o addopts=--cov=api/views --cov-report  html --reuse-db
