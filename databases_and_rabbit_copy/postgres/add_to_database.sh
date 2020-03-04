#!/bin/bash

#psql -U postgres < postgres_out.pgsql

cat xa* > policies.pgsql
psql -U postgres < policies.pgsql
rm policies.pgsql
