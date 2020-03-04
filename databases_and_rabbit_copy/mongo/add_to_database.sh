#!/bin/bash

# you must have mongo server running

mongoimport --db twitter --collection tweets --file tweets.json
mongoimport --db twitter --collection messages --file messages.json
cat xa* > users.json
mongoimport --db twitter --collection users --file users.json
rm users.json
