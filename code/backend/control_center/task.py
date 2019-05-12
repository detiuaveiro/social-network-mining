from enum import IntEnum
from mongo_api import MongoAPI
from postgreSQL import postgreSQL_API
from policy_api import PolicyAPI

class MessageTypes(IntEnum):
    USER_FOLLOWED = 1
    TWEET_LIKED = 2
    TWEET_RETWEETDED = 3
    TWEET_REPLIED = 4
    REQUEST_TWEET_LIKE = 5
    REQUEST_TWEET_RETWEET = 6
    REQUEST_TWEET_REPLY = 7
    REQUEST_FOLLOW_USER = 8
    SAVE_USER = 9
    SAVE_TWEET = 10
    SAVE_LOG = 11

class Task():
    def __init__(self):
        self.mongo = MongoAPI()
        self.postgreSQL = postgreSQL_API("Tweets")
        self.policy = PolicyAPI()

    def menu(self, message_type, message):
        if (message_type == MessageTypes.USER_FOLLOWED):
            pass
        elif (message_type == MessageTypes.TWEET_LIKED):
            pass
        elif (message_type == MessageTypes.TWEET_RETWEETDED):
            pass
        elif (message_type == MessageTypes.TWEET_REPLIED):
            pass
        elif (message_type == MessageTypes.REQUEST_TWEET_LIKE):
            self.policy.lifecycle()
        elif(message_type == MessageTypes.REQUEST_TWEET_RETWEET):
            self.policy.lifecycle()
        elif(message_type == MessageTypes.REQUEST_TWEET_REPLY):
            self.policy.lifecycle()
        elif(message_type == MessageTypes.REQUEST_FOLLOW_USER):
            self.policy.lifecycle()
        elif(message_type == MessageTypes.SAVE_USER):
            print('--------------- Saving User ---------------')
            self.mongo.save('users', message['data'])
        elif(message_type == MessageTypes.SAVE_TWEET):
            print('--------------- Saving Tweet ---------------')
            self.mongo.save('tweets', message['data'])
            self.postgreSQL.insertDataTweets(message['data']['timestamp'],message['data']['id'],message['data']['user_id'],message['data']['likes_count'],message['data']['retweets_count'])
        elif(message_type == MessageTypes.SAVE_LOG):
            self.mongo.save("logs", message['data'])
