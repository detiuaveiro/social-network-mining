#import policy_api
# import policy_api
import logging
import sys

from mongo_wrapper import MongoAPI
from neo4j_wrapper import Neo4jAPI

sys.path.append("../policies")
from enums import *
from PEP import PEP

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
        self.mongo_client = MongoAPI()
        self.neo4j_client = Neo4jAPI()
        self.pep = PEP()

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
    def follow_user(self, data):
        """
        Action to follow user:
            Calls neo4j to add new relation between bot and user
            Calls postgres_stats to add new log with the action details

        @param data: dict containing bot and the user he's following
        """
        log.info("A bot has started following someone")
        type1 = "BOT" if self.neo4j_client.check_bot_exists(data["bot_id"]) else "USER"
        type2 = "BOT" if self.neo4j_client.check_bot_exists(data["data"]["id"]) else "USER"
        self.neo4j_client.add_relationship({
            "id_1": data["bot_id"],
            "id_2": data["data"]["id"],
            "type1": type1,
            "type2": type2
        })
        #falta pro postgres2

    def like_tweet(self, data):
        """
        Action to like tweet:
            Calls postgres_stats to add new log
        
        @param data dict with the bot id and the tweet he liked
        """
        pass

    def retweet(self, data):
        """
        Action to retweet:
            Calls postgres_stats to add new log

        @param data: dict containing bot and the tweet he retweeted
        """
        pass

    def reply_tweet(self, data):
        """
        Action to reply a tweet:
            Calls progres_stats to add what the bot replied and to which tweet

        @param data: dict contaning bot and the reply they made
        """
        pass

    def request_tweet_like(self, data):
        """
        Action to request a like on tweeter:
            Calls the PEP to request a like
            Adds the log to postgres_stats, for the request and its result
            The result is based on the PDP methods
        
        @param data: dict containing the bot id and the tweet id
        """
        log.info("Request a like to a tweet")
        #add log to postgres
        request_accepted = self.pep.receive_message({
                "type": PoliciesTypes.REQUEST_TWEET_LIKE,
                "bot_id": data['bot_id'],
                "user_id": data['data']['user'],
                "tweet_id": data['data']['id'],
                "tweet_text": data['data']['text'],
                "tweet_entities": data['data']['entities']
            })

        if request_accepted:
            log.info("Like request accepted")
            #add log
            self.send(data['bot_id'], ResponseTypes.LIKE_TWEETS, data['data']['id'])
        else:
            log.warning("Like request denied")
            #add log


    def request_retweet(self, data):
        """
        Action to request a retweet:
            Calls the PEP to request the retweet
            Adds the log to postgres_stats, for the request and its result
            The result is based on the PDP methods
        
        2param data: dict containing the bot id and the tweet id
        """
        log.info("Request a retweeting a tweet")
        #add log to postgres
        request_accepted = self.pep.receive_message({
                "type": PoliciesTypes.REQUEST_TWEET_RETWEET,
                "bot_id": data['bot_id'],
                "user_id": data['data']['user'],
                "tweet_id": data['data']['id'],
                "tweet_text": data['data']['text'],
                "tweet_entities": data['data']['entities']
            })

        if request_accepted:
            log.info("Retweet request accepted")
            #add log
            self.send(data['bot_id'], ResponseTypes.RETWEET_TWEETS, data['data']['id'])
        else:
            log.warning("Retweet request denied")
            #add log

    def request_tweet_reply(self, data):
        """
        Action to request a reply:
            Calls the control center to request the reply
            Adds the log to postgres_stats, for the request and its result
            The result is based on the Policy API object
        
        @param data: dict containing the bot id and the tweet id
        """
        log.info("Request a reply to a tweet")
        #add log to postgres
        request_accepted = self.pep.receive_message({
                "type": PoliciesTypes.REQUEST_TWEET_REPLY,
                "bot_id": data['bot_id'],
                "tweet_id": data['data']['id'],
                "user_id": data['data']['user'],
                "tweet_text": data['data']['text'],
                "tweet_entities": data['data']['entities'],
                "tweet_in_reply_to_status_id_str": data['data']['in_reply_to_status_id_str'],
                "tweet_in_reply_to_user_id_str": data['data']['in_reply_to_user_id_str'],
                "tweet_in_reply_to_screen_name": data['data']['in_reply_to_screen_name']
            })

        if request_accepted:
            log.info("Like request accepted")
            #add log
            self.send(data['bot_id'], ResponseTypes.POST_TWEETS, data['data']['id'])
        else:
            log.warning("Like request denied")
            #add log

    def request_follow_user(self, data):
        """
        Action to request a follow:
            Calls the control center to request the follow
            Adds the log to postgres_stats, for the request and its result
            The result is based on the Policy API object
        
        @param data: dict containing the bot id and the tweet id
        """
        log.info("Request a like to a tweet")
        #add log to postgres
        request_accepted = self.pep.receive_message({
                "type": PoliciesTypes.REQUEST_FOLLOW_USER,
                "bot_id": data['bot_id'],
                "user_id": data['data']['id']
            })

        if request_accepted:
            log.info("Like request accepted")
            #add log
            self.send(data['bot_id'], ResponseTypes.FOLLOW_USERS, data['data']['id'])
        else:
            log.warning("Like request denied")
            #add log

    def save_user(self, data):
        """
        Stores info about a user:
            Calls the neo4j and the mongo object to update or store the user be it a bot or a user)
            Adds the log of the operation to postgress_stats
            If the user is a bot, must also call the Policy API object
        
        @param data: dict containing the id of the bot and the user object
        """

        log.info("Saving User")
        pass

    def save_tweet(self, data):
        """
        Stores info about a tweet:
            Calls the mongo object to save or update a tweet
            Adds the operation log to postgress_stats
        
        @param data: dict containing the id of the tweet to bee saved
        """
        pass

    def save_dm(self, data):
        """
        Stores the info about a direct message:
            Calls the mongo object to save or update a dm
            Adds the operation log to postgress_stats
        
        @param data: dict containignt the id of the bot and the dm
        """
        pass

    def error(self, data):
        """
        Stores error that may have occured in the running of a bot:
            Calls the postgres stats to log the error
        
        @param data: dict with the id of a bot and the error object
        """
        pass

    def find_followers(self, data):
        """
        Saves the followers for a given user in the graph database:
            May need to create the user and its followers from scratch or just update their respective info
        
        params
        ------
        data: dict with the id of a user and a list of user IDs
        """
        pass

    def send(self, bot, message_type, params):
        """
        Function the task uses to send messages through rabbit

        @param bot: id of the bot to reply
        @param message_type: ResponseTypes object with the type of message
        @param params: dict with arguments of the message
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
