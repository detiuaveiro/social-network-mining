from Mongo.mongo_api import MongoAPI
from Postgres.postgreSQL import postgreSQL_API
from send import RabbitSend
from policy_api import PolicyAPI
from Neo4j.neo4j_api import Neo4jAPI
from Enums.enums import MessageTypes, Neo4jTypes, PoliciesTypes, ResponseTypes
import logging
import sys

log = logging.getLogger('Task')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)


def send_reply(*, bot_id, message_type, params):
    """

    Parameters
    ----------
    bot_id :
        Id of the bot to reply to
    message_type : ResponseTypes
        Type of the message
    params : dict
        Arguments of the message
    """
    log.info(f"Sending {message_type.name} to Bot with ID: <{bot_id}>")
    log.debug(f"Content: {params}")
    payload = {
        "type": message_type,
        "params": params
    }
    try:
        conn = RabbitSend(host='mqtt-redesfis.5g.cn.atnog.av.it.pt', port=5672, vhost="PI",
                                 username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')
        conn.send(routing_key='tasks.twitter.' + bot_id, message=payload)
        conn.close()
    except Exception as e:
        log.error("FAILED TO SEND MESSAGE")

class Task:
    """Class which represents a Task for a bot to perform."""

    def __init__(self):
        """
        Create a new Task.
        """
        self.mongo = MongoAPI()
        self.postgreSQL = postgreSQL_API("postgres")
        self.postgreSQL2 = postgreSQL_API("policies")
        self.neo4j = Neo4jAPI()
        self.policy = PolicyAPI()

    def menu(self, message_type, message):
        """
        Performs a certain action based on the type of message received.

        Parameters
        ----------
        message_type : MessageTypes
            The type of the message.
        message : dict
            The content of the message.
        """

        if (message_type == MessageTypes.USER_FOLLOWED):
            self.User_Followed(message=message)

        elif (message_type == MessageTypes.TWEET_LIKED):
            self.Tweet_Liked(message=message)

        elif (message_type == MessageTypes.TWEET_RETWEETDED):
            self.Tweet_Retweeted(message=message)

        elif (message_type == MessageTypes.TWEET_REPLIED):
            self.Tweet_Replied(message=message)

        elif (message_type == MessageTypes.REQUEST_TWEET_LIKE):
            self.Request_Tweet_Like(message=message)

        elif(message_type == MessageTypes.REQUEST_TWEET_RETWEET):
            self.Request_Tweet_Retweet(message=message)

        elif(message_type == MessageTypes.REQUEST_TWEET_REPLY):
            self.Request_Tweet_Reply(message=message)

        elif(message_type == MessageTypes.REQUEST_FOLLOW_USER):
            self.Request_Follow_User(message=message)

        elif(message_type == MessageTypes.SAVE_USER):
            self.Save_User(message=message)

        elif(message_type == MessageTypes.SAVE_TWEET):
            self.Save_Tweet(message=message)

        elif(message_type == MessageTypes.ERROR_BOT):
            self.Error_Bot(message=message)

        elif(message_type == MessageTypes.FIND_FOLLOWERS):
            self.Find_Followers(message=message)

    def User_Followed(self, message):
        """
        Stores information about a bot following a user.

        Parameters
        ----------
        message : dict
            A dictionary with the user being followed and the bot following them.
        """
        log.info("TASK: CREATE RELATION BOT -> USER")
        self.neo4j.task(query_type=Neo4jTypes.CREATE_RELATION_BOT_USER,data={"bot_id": message['bot_id'], "user_id": message['data']['id']})
        self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "USER (ID: "+str(message['data']['id'])+" ) FOLLOWED BY BOT (ID: "+str(message['bot_id'])+")"})

    def Tweet_Liked(self, message):
        """
        Stores information about a bot liking a certain tweet.

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot that liked a certain tweet and the id of the tweet
        """
        log.info("TASK: LOGGING TWEET LIKED")
        self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET LIKED (ID: "+str(message['data']['id'])+" )"})

    def Tweet_Retweeted(self, message):
        """
        Stores information about a retweet made by a certain bot.

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot and the retweet they made.
        """
        log.info("TASK: LOG TWEET RETWEETED")
        self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET RETWEETED (ID: "+str(message['data']['id'])+" )"})

    def Tweet_Replied(self, message):
        """
        Stores information about a reply by a bot to a certain tweet

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot and the reply they made.
        """
        log.info("TASK: LOG TWEET REPLIED")
        self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET REPLIED (ID: "+str(message['data']['id'])+" )"})

    def Request_Tweet_Like(self, message):
        """
        Requests the control center permission to like a certain tweet.

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot and the id of the tweet they want to like
        """
        log.info("TASK: REQUEST LIKE TWEET")
        self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "REQUEST TO LIKE TWEET (ID: "+str(message['data']['id'])+" )"})

        result = self.policy.lifecycle(msg={
            "type": PoliciesTypes.REQUEST_TWEET_LIKE,
            "bot_id": message['bot_id'],
            "user_id": message['data']['user'],
            "tweet_id": message['data']['id'],
            "tweet_text": message['data']['text'],
            "tweet_entities": message['data']['entities']
        })
        if (result==1):
            log.info("TWEET ACCEPTED TO BE LIKED")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) ALLOWED TO BE LIKED"})
            send_reply(bot_id=message['bot_id'], message_type=ResponseTypes.RETWEET_TWEETS,
                       params=message['data']['id'])
        else:
            log.info("TWEET NOT ACCEPTED TO BE LIKED")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) NOT ALLOWED TO BE LIKED"})

    def Request_Tweet_Retweet(self, message):
        """
        Requests the control center permission to retweet a certain tweet.

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot and the id of the tweet they want to retweet
        """
        log.info("TASK: REQUEST RETWEET TWEET")
        self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "REQUEST TO RETWEET TWEET (ID: "+str(message['data']['id'])+" )"})
        result = self.policy.lifecycle(msg={
            "type": PoliciesTypes.REQUEST_TWEET_RETWEET,
            "bot_id": message['bot_id'],
            "user_id": message['data']['user'],
            "tweet_id": message['data']['id'],
            "tweet_text": message['data']['text'],
            "tweet_entities": message['data']['entities']
        })
        if (result==1):
            log.info("TWEET ACCEPTED TO BE RETWEETED")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) ALLOWED TO BE RETWEETED"})
            send_reply(bot_id=message['bot_id'], message_type=ResponseTypes.RETWEET_TWEETS,
                       params=message['data']['id'])
        else:
            log.info("TWEET NOT ACCEPTED TO BE RETWEETED")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) NOT ALLOWED TO BE RETWEETED"})

    def Request_Tweet_Reply(self, message):
        """
        Requests the control center to reply to a certain tweet.

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot and the id of the tweet they want to reply to
        """
        log.info("TASK: REQUEST REPLY TWEET")
        self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "REQUEST TO REPLY TWEET (ID: "+str(message['data']['id'])+" )"})
        result = self.policy.lifecycle(msg={
            "type": PoliciesTypes.REQUEST_TWEET_REPLY,
            "bot_id": message['bot_id'],
            "tweet_id": message['data']['id'],
            "user_id": message['data']['user'],
            "tweet_text": message['data']['text'],
            "tweet_entities": message['data']['entities'],
            "tweet_in_reply_to_status_id_str": message['data']['in_reply_to_status_id_str'],
            "tweet_in_reply_to_user_id_str": message['data']['in_reply_to_user_id_str'],
            "tweet_in_reply_to_screen_name": message['data']['in_reply_to_screen_name']
        })
        if (result==1):
            log.info("TWEET ALLOWED TO BE REPLIED")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) ALLOWED TO BE REPLIED"})
            send_reply(bot_id=message['bot_id'], message_type=ResponseTypes.REPLY_TWEETS,
                       params=message['data']['id'])
        else:
            log.info("TWEET NOT ALLOWED TO BE REPLIED")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "TWEET (ID: "+str(message['data']['id'])+" ) NOT ALLOWED TO BE REPLIED"})

    def Request_Follow_User(self, message):
        """
        Requests the control center permission to follow a certain user.

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot and the id of the user they want to follow
        """
        log.info("TASK: REQUEST FOLLOW USER")
        self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "REQUEST TO FOLLOW USER ("+str(message['data']['id'])+")"})
        result = self.policy.lifecycle(msg={
            "type": PoliciesTypes.REQUEST_FOLLOW_USER,
            "bot_id": message['bot_id'],
            "user_id": message['data']['id'],
        })
        if (result==1):
            log.info("USER ALLOWED TO BE FOLLOWED")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "USER (ID: "+str(message['data']['id'])+" ) ALLOWED TO BE FOLLOWED"})
            send_reply(bot_id=message['bot_id'], message_type=ResponseTypes.FOLLOW_USERS,
                       params={"type": "id", "data": [message['data']['id']]})

        else:
            log.info("USER NOT ALLOWED TO BE FOLLOWED")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "USER (ID: "+str(message['data']['id'])+" ) NOT ALLOWED TO BE FOLLOWED"})

    def Save_User(self, message):
        """
        Stores the information about a certain user.

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot and the User object as the data
        """
        log.info("TASK: SAVE USER")
        is_bot = False
        if (int(message['bot_id'])==message['data']['id']):
            log.info("USER IS BOT")
            is_bot = True
        if (is_bot):
            exists = self.neo4j.task(Neo4jTypes.SEARCH_BOT,data={"bot_id": message['bot_id']})
            if (exists):
                log.info("BOT ALREADY EXISTS")
                self.mongo.update('users', message['data'])
                self.neo4j.task(Neo4jTypes.UPDATE_BOT,data={"bot_id": message['bot_id'], "bot_name": message['data']['name'], "bot_username": message['data']['screen_name']})
            else:
                log.info("NEW BOT")
                result = self.policy.lifecycle(msg={
                    "type": PoliciesTypes.FIRST_TIME,
                    "bot_id": message['bot_id'],
                })

                send_reply(bot_id=message['bot_id'], message_type=ResponseTypes.FOLLOW_USERS,
                           params={"type": "screen_name", "data": result})
                self.mongo.save('users', message['data'])
                self.neo4j.task(Neo4jTypes.CREATE_BOT,data={"id": message['bot_id'], "name": message['data']['name'], "username": message['data']['screen_name']})
        else:
            exists = self.neo4j.task(Neo4jTypes.SEARCH_USER,data={"user_id": message['data']['id']})
            if (exists):
                log.info("USER ALREADY EXISTS")
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "UPDATING USER INFO ("+str(message['data']['id'])+")"})
                self.mongo.update('users', message['data'])
                self.neo4j.task(Neo4jTypes.UPDATE_USER,data={"user_id": message['data']['id'], "user_name": message['data']['name'], "user_username": message['data']['screen_name']})
            else:
                log.info("NEW USER")
                self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "SAVING NEW USER ("+str(message['data']['id'])+")"})
                self.mongo.save('users', message['data'])
                self.neo4j.task(Neo4jTypes.CREATE_USER,data={"id": message['data']['id'], "name": message['data']['name'], "username": message['data']['screen_name']})
        self.postgreSQL.addUser(mapa={"user_id": message['data']['id'], "followers": message['data']['followers_count'], "following": message['data']['friends_count']})

    def Save_Tweet(self, message):
        """
        Stores the information about a certain tweet.

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot and the tweet object as the data
        """
        log.info("TASK: SAVE TWEET")
        tweet_exists = self.mongo.search('tweets', message['data'])
        if (tweet_exists):
            log.info("TWEET EXISTS")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "UPDATING TWEET STATS ("+str(message['data']['id'])+")"})
            self.mongo.update('tweets', message['data'])
        else:
            log.info("NEW TWEET")
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "SAVING TWEET ("+str(message['data']['id'])+")"})
            self.mongo.save('tweets', message['data'])
        self.postgreSQL.addTweet(mapa={"tweet_id": message['data']['id'], "user_id": message['data']['user'], "likes": message['data']['favorite_count'], "retweets": message['data']['retweet_count']})

    def Error_Bot(self, message):
        """
        Logs a error that may have occurred while a certain bot was running.

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot and the tweet object as the data
        """
        log.info("TASK: ERROR_BOT")           
        self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "WARNING: BOT WITH THE FOLLOWING ID "+str(message['bot_id'])+" GAVE THIS ERROR "+str(message['data']['msg'])})

    def Find_Followers(self, message):
        """
        Saves the followers for a given user in the graph database

        Parameters
        ----------
        message : dict
            A dictionary containing the id of the bot, and a dictionary that maps user ids into a list of their followers
        """
        log.info("TASK: SAVE FOLLOWERS")
        for key, value in message['data'].items():
            self.postgreSQL2.addLog(mapa={"id_bot": message['bot_id'], "action": "SAVE LIST OF USERS FOLLOWED BY USER WITH ID: "+str(key)})
            for user2 in value:
                self.neo4j.task(query_type=Neo4jTypes.CREATE_RELATION_USER_USER,data={"user1": key, "user2": user2})
