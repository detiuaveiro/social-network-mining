# Requirements

## Useful Link
- https://docs.djangoproject.com/en/3.0/topics/db/multi-db/

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