from mongo_api import MongoAPI
from postgreSQL import postgreSQL_API

class WIW:
    """Class which represents a Task for a bot to perform."""

    def __init__(self):
        """
        Create a new Task.
        """
        self.mongo = MongoAPI()
        self.postgreSQL = postgreSQL_API("postgres")
        self.okay_users = []
        self.bad_users = []
        self.okay_tweets = []
        self.bad_tweets = []

    def users_check(self):
        good_users_count = 0
        mongo_users = self.mongo.getUsers()
        postgres_users = self.postgreSQL.getAllStatsUsers()
        for p_user in postgres_users:
            if (str(p_user['user_id']) in self.okay_users):
                continue
            tried_users=0
            for m_user in mongo_users:
                print(p_user)
                print(m_user)
                if (str(p_user['user_id'])==str(m_user['id'])):
                    self.okay_users.append(str(p_user['user_id']))
                    good_users_count += 1
                    print(len(self.okay_users))
                else:
                    tried_users += 1
                    if (tried_users==len(mongo_users)):
                        self.bad_users.append(str(p_user['user_id']))
                        print(len(self.bad_users))

    def tweets_check(self):
        good_tweets_count = 0
        mongo_tweets = self.mongo.getTweets()
        postgres_tweets = self.postgreSQL.getAllStatsTweets()
        for p_tweet in postgres_tweets:
            if (str(p_tweet['tweet_id']) in self.okay_tweets):
                continue
            tried_tweets=0
            for m_tweet in mongo_tweets:
                print(p_tweet)
                print(m_tweet)
                if (str(p_tweet['tweet_id'])==str(m_tweet['id'])):
                    self.okay_tweets.append(str(p_tweet['tweet_id']))
                    good_tweets_count += 1
                    print(len(self.okay_tweets))
                else:
                    tried_tweets += 1
                    if (tried_tweets==len(mongo_tweets)):
                        self.bad_tweets.append(str(p_tweet['tweet_id']))
                        print(len(self.bad_tweets))

    def printAll(self):
        print(self.bad_users)
        print(self.bad_tweets)

if __name__ == "__main__":
    n = WIW()
    n.users_check()
    n.tweets_check()
    
