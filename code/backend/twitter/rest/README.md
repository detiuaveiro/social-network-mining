
# Examples
## Tweet object

 - On backend/twitter/examples/tweet_object.json
 - How to add to mongo
 ```mongo
 > use twitter
 > db.createCollection("tweets")
 > db.tweets.insert([<content on backend/twitter/examples/tweet_object.json>])
 ```

 ## ATENTION!
 - When we are inserting a new tweet object, it is necessary that all arguments defined on the django models are placed (even if their value is set to null), because of the db integrety 
 - The twitter id's with wish we are working on the rest api correspond to the str_id of the tweets objects





 

```
$ pip install djongo
```

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
2. Using admin user , create another user (django user)
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

##Postgres

- psycopg2 (postgresql's API)
```
pip install django psycopg2
```

- Create user (for development)
```
$ sudo su postgres -c psql
$ create database twitter_postgre;
$ create user admin with password 'admin';
$ GRANT ALL PRIVILEGES ON DATABASE twitter_postgre TO admin;
```

- Access DB (after user creation)
```
$ psql -d twitter_postgre -U admin -W 
```

docker run -p 80:80 \
    -e 'PGADMIN_DEFAULT_EMAIL=rafaeljsimoes@gmail.com' \
    -e 'PGADMIN_DEFAULT_PASSWORD=admin' \
    -d dpage/pgadmin4

