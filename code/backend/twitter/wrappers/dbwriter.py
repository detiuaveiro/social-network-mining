import mongo
import neo4j
import postgres
import rabbitmq
#import policy_api
import logging
import sys
sys.path.append("..")
from enums import *

log = logging.getLogger('Database Writer')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)

class DBWriter:
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

        if message_type == MessageTypes.USER_FOLLOWED:
            self.follow_user(message)

        elif message_type == MessageTypes.TWEET_LIKED:
            self.like_tweet(message)

        elif message_type == MessageTypes.TWEET_RETWEETDED:
            self.retweet(message)

        elif message_type == MessageTypes.TWEET_REPLIED:
            self.reply_tweet(message)

        elif message_type == MessageTypes.REQUEST_TWEET_LIKE:
            self.request_tweet_like(message)

        elif message_type == MessageTypes.REQUEST_TWEET_RETWEET:
            self.request_retweet(message)

        elif message_type == MessageTypes.REQUEST_TWEET_REPLY:
            self.request_tweet_reply(message)

        elif message_type == MessageTypes.REQUEST_FOLLOW_USER:
            self.request_follow_user(message)

        elif message_type == MessageTypes.SAVE_USER:
            self.save_user(message)

        elif message_type == MessageTypes.SAVE_TWEET:
            self.save_tweet(message)

        elif message_type == MessageTypes.SAVE_DIRECT_MESSAGES:
            self.save_dm(message)
    
        elif message_type == MessageTypes.ERROR_BOT:
            self.error(message)

        elif message_type == MessageTypes.FIND_FOLLOWERS:
            self.find_followers(message)


    #Need DB API now
    def follow_user(self, message):
        """
        Action to follow user:
            Calls neo4j to add new relation between bot and user
            Calls postgres_stats to add new log with the action details

        params:
        ------
        message: dict containing bot and the user he's following
        """
        pass

    def like_tweet(self, message):
        """
        Action to like tweet:
            Calls postgres_stats to add new log
        
        params:
        -------
        message: dict with the bot id and the tweet he liked
        """
        pass

    def retweet(self, message):
        """
        Action to retweet:
            Calls postgres_stats to add new log

        params:
        ------
        message: dict containing bot and the tweet he retweeted
        """
        pass

    def reply_tweet(self, message):
        """
        Action to reply a tweet:
            Calls progres_stats to add what the bot replied and to which tweet

        params:
        ------
        message: dict contaning bot and the reply they made
        """
        pass

    def request_tweet_like(self, message):
        """
        Action to request a like on tweeter:
            Calls the control center to request the like
            Adds the log to postgres_stats, for the request and its result
            The result is based on the Policy API object
        
        params:
        ------
        message: dict containing the bot id and the tweet id
        """
        pass

    def request_retweet(self, message):
        """
        Action to request a retweet:
            Calls the control center to request the retweet
            Adds the log to postgres_stats, for the request and its result
            The result is based on the Policy API object
        
        params:
        ------
        message: dict containing the bot id and the tweet id
        """
        pass

    def request_tweet_reply(self, message):
        """
        Action to request a reply:
            Calls the control center to request the reply
            Adds the log to postgres_stats, for the request and its result
            The result is based on the Policy API object
        
        params:
        ------
        message: dict containing the bot id and the tweet id
        """
        pass

    def request_follow_user(self, message):
        """
        Action to request a follow:
            Calls the control center to request the follow
            Adds the log to postgres_stats, for the request and its result
            The result is based on the Policy API object
        
        params:
        ------
        message: dict containing the bot id and the tweet id
        """
        pass

    def save_user(self, message):
        """
        Stores info about a user:
            Calls the neo4j and the mongo object to update or store the user be it a bot r a user)
            Adds the log of the operation to postgress_stats
            If the user is a bot, must also call the Policy API object
        params:
        ------
        message: dict containing the id of the bot and the user object
        """
        pass

    def save_tweet(self, message):
        """
        Stores info about a tweet:
            Calls the mongo object to save or update a tweet
            Adds the operation log to postgress_stats
        params
        ------
        message: dict containing the id of the tweet to bee saved
        """
        pass

    def save_dm(self, message):
        """
        Stores the info about a direct message:
            Calls the mongo object to save or update a dm
            Adds the operation log to postgress_stats
        params
        ------
        message: dict containignt the id of the bot and the dm
        """
        pass

    def error(self, message):
        """
        Stores error that may have occured in the running of a bot:
            Calls the postgres stats to log the error
        params
        ------
        message: dict with the id of a bot and the error object
        """
        pass

    def find_followers(self, message):
        """
        Saves the followers for a given user in the graph database:
            May need to create the user and its followers from scratch or just update their respective info
        
        params
        ------
        message: dict with the id of a user and a list of user IDs
        """
        pass

    def send(self, bot, message_type, params):
        """
        Function the task uses to send messages through rabbit

        params
        ------
        bot: id of the bot to reply
        message_type: ResponseTypes object with the type of message
        params: dict with arguments of the message
        """
        log.info(f"Sending {message_type.name} to Bot with ID: <{bot}>")
        log.debug(f"Content: {params}")
        payload = {
            "type": message_type,
            "params": params
        }
        try:
            conn = Rabbitmq()
            conn.send(routing_key='tasks.twitter.' + bot_id, message=payload)
            conn.close()
        except:
            log.error("FAILED TO SEND MESSAGE:")
