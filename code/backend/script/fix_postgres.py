from mongo_api import MongoAPI
from postgreSQL import postgreSQL_API

class Fix:
    """Class which represents a Task for a bot to perform."""

    def __init__(self):
        """
        Create a new Task.
        """
        self.mongo = MongoAPI()
        self.postgreSQL = postgreSQL_API("postgres")
        self.errors_users = []
        self.errors_tweets = []

    def save_to_postgres(self):
        mongo_users = self.mongo.getUsers()
        for user in mongo_users:
            try:
                self.postgreSQL.addUser(mapa={"user_id": user['id'], "followers": user['followers_count'], "following": user['friends_count']})
            except:
                self.errors_users.append(user['id'])
        mongo_tweets = self.mongo.getTweets()
        for tweet in mongo_tweets:
            try:
                self.postgreSQL.addTweet(mapa={"tweet_id": tweet['id'], "user_id": tweet['user'], "likes": tweet['favorite_count'], "retweets": tweet['retweet_count']})
            except:
                self.errors_tweets.append(tweet['id'])

        print(self.errors_users)
        print("----------------")
        print(self.errors_tweets)

if __name__ == "__main__":
    n = Fix()
    n.save_to_postgres()
    

