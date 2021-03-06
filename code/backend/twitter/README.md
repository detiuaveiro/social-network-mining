# Attention! Hotfix in PostgreSQL required
Entrei no psql pelo comando 
``psql -U admin -W -d twitter``

E escrevam o comando
``ALTER TABLE logs ADD COLUMN target_id bigint;``

# Examples
## Tweet object

 - On backend/twitter/examples/tweet_object.json
 - How to add to mongo:
 ```mongo
 > use twitter
 > db.createCollection("tweets")
 > db.tweets.insert([<content on backend/twitter/examples/tweet_object.json>])
 ```

## User object

 - On backend/twitter/examples/user_object.json
 - How to add to mongo:
 ```mongo
 > use twitter
 > db.createCollection("users")
 > db.users.insert([<content on backend/twitter/examples/users_object.json>])
 ```

 ## ATENTION!
 - When we are inserting a new tweet object, it is necessary that all arguments defined on the django models are placed (even if their value is set to null), because of the db integrety 
 - The twitter id's with wish we are working on the rest api correspond to the str_id of the tweets objects


# Django MultiDBS and DBs configuration
## Useful Link
- https://docs.djangoproject.com/en/3.0/topics/db/multi-db/

## Makemigrations and migrate operations
- Now its necessary define which db you want to do migrate operation, because default DB it is not defined
- DB Names are defined on DATABASES dictionary (keys) on settings.py 

```
$ rm -rf api/migrations
$ python3 manage.py makemigrations api
$ python3 manage.py migrate --database postgres <or>  python3 manage.py migrate --database mongo 
```


## Mongo
- Create user (for development)
1. Create a user admin (to manage other users)
```
$ mongo
$ use admin;
$     db.createUser(
      {
        user: "admin",
        pwd: "admin",
        roles: [ { role: "root", db: "admin" } ]
      }
    )
```
2. Using admin user, create another user (django user)
```
$ mongo --port 27017 -u "admin" -p "admin" --authenticationDatabase "admin"
$ use twitter;
$     db.createUser(
      {
        user: "admin",
        pwd: "admin",
        roles: [ { role: "dbOwner" , db: "twitter" } ]
      }
    )
```

- Access DB (after user creation)
```
mongo --port 27017 -u "admin" -p "admin" --authenticationDatabase "twitter"
```

## Postgres

- Create user (for development)
```postgresql
$ sudo su postgres -c psql
# create database postgres;
# create user admin with password 'admin';
# GRANT ALL PRIVILEGES ON DATABASE postgres TO admin;
# \c postgres
# GRANT ALL ON ALL TABLES IN SCHEMA public to admin;
# GRANT ALL ON ALL SEQUENCES IN SCHEMA public to admin;
# GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to admin;
```

- Access DB (after user creation)
```
$ psql -d twitter_postgres -U admin -W 
```


# Policies Object
- Items:
    - id : int
    - API_type : str (TWITTER OR INSTAGRAM)
    - filter : str (USERNAME OR KEYWORDS)
    - name : str
    - tags : str[]
    - bots : int[]
- Example in dictionary
```
{ "id" : 1, "API_type": "Twitter", "filter": "Target", "name": "Politica", "tags": ["PSD", "CDS"], "bots": [1, 2] }
```

# Documentation
## Swagger
You can check the documentation created for the REST API through the link:
 - *URL*/documentation
It should automatically change without any further commands

## Doxyfile
You can check the documentation created for the other python modules by searching for the index.html file in the Documentation subdirectory

To redo the documentation, use the command:
```
$ doxygen Doxyfile
```