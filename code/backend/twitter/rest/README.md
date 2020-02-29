# Requirements

- djongo (mongo's API)

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
