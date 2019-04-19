from enum import IntEnum
from mongo_api import MongoAPI

class MessageTypes(IntEnum):
    USER_FOLLOWED = 1
    REQUEST_TWEET_LIKE = 2
    REQUEST_TWEET_RETWEET = 3
    REQUEST_TWEET_REPLY = 4
    REQUEST_FOLLOW_USER = 5
    SAVE_USER = 6
    SAVE_TWEET = 7

class Task():
    def __init__(self):
        self.mongo = MongoAPI()

    def menu(self, message_type, message):
        if (message_type == MessageTypes.USER_FOLLOWED):
            pass
        elif (message_type == MessageTypes.REQUEST_TWEET_LIKE):
            pass
        elif(message_type == MessageTypes.REQUEST_TWEET_RETWEET):
            pass
        elif(message_type == MessageTypes.REQUEST_TWEET_REPLY):
            pass
        elif(message_type == MessageTypes.REQUEST_FOLLOW_USER):
            pass
        elif(message_type == MessageTypes.SAVE_USER):
            print('--------------- Saving User ---------------')
            self.mongo.save('users', message['data'])
        elif(message_type == MessageTypes.SAVE_TWEET):
            print('--------------- Saving Tweet ---------------')
            self.mongo.save('tweets', message['data'])