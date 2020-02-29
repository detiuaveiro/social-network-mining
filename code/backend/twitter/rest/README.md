
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
