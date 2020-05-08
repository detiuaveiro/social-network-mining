mkdir mongodb
mkdir postgresql


echo "Importing mongo DB"
mongoexport --collection tweets  --db twitter --out "mongodb/tweets.json" --authenticationDatabase admin -u $MONGO_USERNAME -p $MONGO_PASSWORD --host "192.168.85.46:27017" 
mongoexport --collection messages  --db twitter --out "mongodb/messages.json" --authenticationDatabase admin  -u $MONGO_USERNAME -p $MONGO_PASSWORD --host "192.168.85.46:27017"
mongoexport --collection users  --db twitter --out "mongodb/users.json" --authenticationDatabase admin -u $MONGO_USERNAME -p $MONGO_PASSWORD --host "192.168.85.46:27017" 

echo "Deleting local mongo DB data"
mongo twitter -u $MONGO_USERNAME_LOCAL -p $MONGO_PASSWORD_LOCAL --host "localhost:27017" --eval "db.dropDatabase()" 

echo "Loading mongo DB data locally"
mongoimport --collection tweets  --db twitter --file  "mongodb/tweets.json" --authenticationDatabase admin -u $MONGO_USERNAME_LOCAL -p $MONGO_PASSWORD_LOCAL --host "localhost:27017"
mongoimport --collection messages  --db twitter --file  "mongodb/messages.json" --authenticationDatabase admin -u $MONGO_USERNAME_LOCAL -p $MONGO_PASSWORD_LOCAL --host "localhost:27017"
mongoimport --collection users  --db twitter --file  "mongodb/users.json" --authenticationDatabase admin -u $MONGO_USERNAME_LOCAL -p $MONGO_PASSWORD_LOCAL --host "localhost:27017"


echo "Importing postgresql DB"
PGPASSWORD=$POSTGRES_PASSWORD pg_dump -d twitter -U $POSTGRES_USERNAME -h "192.168.85.46" > postgresql/twitter.pgsql

echo "Deleting local postgresql DB data"
PGPASSWORD=$POSTGRES_PASSWORD_LOCAL psql -d twitter -U $POSTGRES_USERNAME_LOCAL -h "localhost" -c "drop table logs,policies,tweets,users;"

echo "Loading postgresql DB data locally"
PGPASSWORD=$POSTGRES_PASSWORD_LOCAL psql -d twitter -U $POSTGRES_USERNAME_LOCAL -h "localhost" < postgresql/twitter.pgsql
