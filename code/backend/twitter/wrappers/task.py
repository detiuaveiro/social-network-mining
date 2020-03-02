import mongo
import neo4j
import postgres
import rabbitmq
#import policy_api
import logging
import sys
sys.path.append("..")
from enums import *

log = logging.getLogger('Task')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)

class Task:
"""
Class to simulate the behaviour of a bot:
On receiving a message from a message broker, this class will act accordingly
"""
    def __init__(self):
        """
        This will start instaces for all the DB's API
        """
        #Falta as API
        #...
        pass

    def action(self, message):
        message_type = message['type']

        if (message_type == MessageTypes.USER_FOLLOWED):
            self.follow_user(message)

        elif (message_type == MessageTypes.TWEET_LIKED):
            self.like_tweet(message)

        elif (message_type == MessageTypes.TWEET_RETWEETDED):
            self.retweet(message)

        elif (message_type == MessageTypes.TWEET_REPLIED):
            self.reply_tweet(message)

        elif (message_type == MessageTypes.REQUEST_TWEET_LIKE):
            self.request_tweet_like(message)

        elif(message_type == MessageTypes.REQUEST_TWEET_RETWEET):
            self.request_retweet(message)

        elif(message_type == MessageTypes.REQUEST_TWEET_REPLY):
            self.request_tweet_reply(message)

        elif(message_type == MessageTypes.REQUEST_FOLLOW_USER):
            self.request_follow_user(message)

        elif(message_type == MessageTypes.SAVE_USER):
            self.save_user(message)

        elif(message_type == MessageTypes.SAVE_TWEET):
            self.save_tweet(message)

        elif(message_type == MessageTypes.ERROR_BOT):
            self.error(message)

        elif(message_type == MessageTypes.FIND_FOLLOWERS):
            self.find_followers(message)

        elif(message_type == MessageTypes.SAVE_DIRECT_MESSAGES):
            self.save_dm(message)

    #Need DB API now