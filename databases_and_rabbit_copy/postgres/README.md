# How to add everything to mongo database

## Requirements
 - You have to have installed on your machine `postgresql <12` and `timescaledb`

## Run
```bash
$ echo "shared_preload_libraries = 'timescaledb'" >> /var/lib/postgres/data/postgresql.conf
$ chmod u+x add_to_database.sh
$ ./add_to_database.sh
```
