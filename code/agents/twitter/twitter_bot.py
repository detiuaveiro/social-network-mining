import argparse
import logging
import os
from typing import List, Dict, Any, Union
import sys

import tweepy
from pyrabbit2 import Client

import settings
import utils
from api import TweepyWrapper
from cache import Cache
from enums import Task, MessageType
from exceptions import NoMessagesInQueue
from models import User, Tweet, BaseModel

log = logging.getLogger("bot-agents")
log.setLevel(logging.DEBUG)


class TwitterBot:
    def __init__(self, bot_id, messaging_manager: Client, api: tweepy.API):
        self._id = bot_id
        self.messaging = messaging_manager
        self._api = api
        self.user: User
        self._cache: Cache = Cache(f"cache_{self._id}", logger=log)
        self.vhost = settings.VHOST
        # Name of the exchange to receive the tasks
        self.tasks_exchange: str = settings.TASKS_EXCHANGE
        # Name of the queue we're going to use to receive the tasks
        self.tasks_queue = f"{settings.TASKS_QUEUE_PREFIX}-{self._id}"
        self.tasks_routing_key = f"{settings.TASKS_ROUTING_KEY_PREFIX}.{self._id}"
        # Name of the exchange to upload the actions
        self.query_exchange = settings.QUERY_EXCHANGE
        self.query_routing_key = settings.QUERY_ROUTING_KEY
        # Name of the exchange to upload the logs
        self.log_exchange = settings.LOG_EXCHANGE
        self.log_routing_key = settings.LOG_ROUTING_KEY
        # Name of the exchange to upload data
        self.data_exchange = settings.DATA_EXCHANGE
        self.data_routing_key = settings.DATA_ROUTING_KEY
        # Last Tweet read
        self.last_home_tweet: int = None
        # no comments
        self._api.create_favourite = self._api.create_favorite

    def __repr__(self):
        return f"<TwitterBot id={self._id}, messaging_manager={self.messaging}, api={self._api}>"

    def _setup_messaging(self):
        """
            Private method for setuping the messaging connections
        """
        log.debug("Setting up Messaging to: Receive Tasks")
        log.debug(f"Connecting to exchange {self.tasks_exchange}")
        self.messaging.create_exchange(vhost=self.vhost, name=self.tasks_exchange, xtype="direct")
        log.debug(f"Creating queue {self.tasks_queue}")
        self.messaging.create_queue(vhost=self.vhost, name=self.tasks_queue)
        log.debug(f"Binding exchange to queue {self.tasks_queue} with key {self.tasks_routing_key}")
        self.messaging.create_binding(vhost=self.vhost, exchange=self.tasks_exchange,
                                      queue=self.tasks_queue, rt_key=self.tasks_routing_key)
        log.info("---------------------------------------")
        log.info(
            f"Connected to Messaging Service using: exchange={self.tasks_exchange}, queue={self.tasks_queue}, routing_key={self.tasks_routing_key}")
        log.info("Ready to receive tasks")

        log.debug("---------------------------------------")
        log.debug("Setting up Messaging to: Upload Logs")
        log.debug(f"Connecting to exchange {self.log_exchange}")
        self.messaging.create_exchange(vhost=self.vhost, name=self.log_exchange, xtype="direct")
        log.info("---------------------------------------")
        log.info(
            f"Connected to Messaging Service using: exchange={self.log_exchange}")
        log.info("Ready to: Upload Logs")

        log.debug("---------------------------------------")
        log.debug("Setting up Messaging to: Make Queries")
        log.debug(f"Connecting to exchange {self.query_exchange}")
        self.messaging.create_exchange(vhost=self.vhost, name=self.query_exchange, xtype="direct")
        log.info("---------------------------------------")
        log.info(
            f"Connected to Messaging Service using: exchange={self.query_exchange}")
        log.info("Ready to: Make Queries")

        log.debug("---------------------------------------")
        log.debug("Setting up Messaging to: Upload Data")
        log.debug(f"Connecting to exchange {self.data_exchange}")
        self.messaging.create_exchange(vhost=self.vhost, name=self.data_exchange, xtype="direct")
        log.info("---------------------------------------")
        log.info(
            f"Connected to Messaging Service using: exchange={self.data_exchange}")
        log.info("Ready to: Upload Data")

    def _setup(self):
        """
            Private method for setting up. Includes setting the messagging queues, checking if the credentials are valid
        """
        log.debug(f"Setting up with: {self}")
        log.debug("---------------------------------------")
        self._setup_messaging()
        log.debug("Verifying credentials")
        self.user: User = self._api.verify_credentials()
        log.debug(f"Logged in as:{self.user}")
        log.debug(f"Sending our user to {self.data_exchange}")
        self.send_user(user=self.user)

        log.debug("Opening Cache")
        self._cache.open()
        log.debug("Checking last Tweet")
        self.last_home_tweet = self._cache.get("last_home_tweet", None)
        log.debug(f"Last Tweet was: <{self.last_home_tweet}>")

    def get_new_message(self):
        """
            Helper message to get a new message from the tasks queue
        """
        msg: List[Dict] = self.messaging.get_messages(vhost=self.vhost, qname=self.tasks_queue,
                                                      count=1)
        if msg and msg[0].get("payload", None):
            return utils.from_json(msg[0]["payload"])
        raise NoMessagesInQueue("Queue has no messages left!")

    def run(self):
        """
        Loop of the bot.
        As simple as a normal handler, tries to get tasks from the queue and, depending on the task, does a different action
        """
        self._setup()
        retries = settings.MAX_RETRIES
        log.debug("Starting to get tasks...")
        while True:
            try:
                log.debug(f"Getting next task from {self.tasks_queue}")
                task_msg = self.get_new_message()
                task_type, task_params = task_msg["type"], task_msg["params"]
                log.debug(f"Received task {task_msg} with:", task_params)
                if task_type == Task.FIND_BY_KEYWORDS:
                    self.find_keywords_routine(task_params["keywords"])
                    pass
                elif task_type == Task.FOLLOW_USERS:
                    self.follow_users_routine(task_params)
                    pass
                elif task_type == Task.LIKE_TWEETS:
                    self.like_tweets_routine(task_params)
                elif task_type == Task.RETWEET_TWEETS:
                    self.retweet_tweets_routine(task_params)
                else:
                    log.warning(f"Received unknown task_msg: {task_msg}")
            except NoMessagesInQueue:
                if retries == 0:
                    break
                log.debug("No Messages found. Waiting...")
                utils.wait_for(5)
                retries -= 1
            except tweepy.error.TweepError as e:
                if e.api_code == 63 or e.api_code == 64:
                    payload = {
                        "type"     : MessageType.EVENT_USER_SUSPENDED,
                        "bot_id"   : self._id,
                        "timestamp": utils.current_time(),
                        "data"     : {
                            "code": e.api_code,
                            "msg" : e.reason
                        },
                    }
                    self.messaging.publish(vhost=self.vhost, xname=self.log_exchange,
                                           rt_key=self.log_routing_key,
                                           payload=utils.to_json(payload))
        self.cleanup()

    def cleanup(self):
        """
        Method for cleaning up any connections.
        TODO: maybe remove this?
        """
        log.warning("TODO: Implement Clean up")
        self._cache.close()

    def like_tweets_routine(self, tweets_ids: Union[int, List[int]]):
        """
        Routine for the LIKE_TWEETS task
        Likes 1 or several tweets, with their ids being the parameters

        Parameters
        ----------
        tweets_ids: `Union[int, List[int]]`
            Either 1 tweet ID or a list of tweet Ids
        """
        log.debug("Starting 'Like Tweets' routine...")


        # Helper function so we don't have to repeat code

        def get_and_like_tweet(tweet_id):
            tweet: Tweet = self._api.get_status(tweet_id=tweet_id)
            if tweet.favorited:
                log.debug(f"Tweet with ID={tweet.id} already liked, no need to like again")
            else:
                log.debug(f"Liking Tweet with ID={tweet.id}")
                tweet.like()
                self.send_event(MessageType.EVENT_TWEET_LIKED, tweet)

        # Single tweet
        if type(tweets_ids) is int:
            get_and_like_tweet(tweet_id=tweet_id)
        # Multiple tweets
        elif type(tweets_ids) is list:
            for tweet_id in tweets_ids:
                get_and_like_tweet(tweet_id=tweet_id)
        # Unknown type
        else:
            log.warn(f"Unknown parameter type received, {type(tweets_ids)} with content: <{tweets_ids}>")

    def retweet_tweets_routine(self, tweets_ids: Union[int, List[int]]):
        """
        Routine for the RETWEET_TWEETS task
        Retweets 1 or several tweets, with their ids being the parameters

        Parameters
        ----------
        tweets_ids: `Union[int, List[int]]`
            Either 1 tweet ID or a list of tweet Ids
        """
        log.debug("Starting 'Retweet Tweets' routine...")

        # Helper function so we don't have to repeat code
        def get_and_retweet_tweet(tweet_id):
            tweet: Tweet = self._api.get_status(tweet_id=tweet_id)
            if tweet.retweeted:
                log.debug(f"Tweet with ID={tweet.id} already retweeted, no need to retweet again")
            else:
                log.debug(f"Retweeting Tweet with ID={tweet.id}")
                tweet.retweet()
                self.send_event(MessageType.EVENT_TWEET_RETWEETED, tweet)

        # Single tweet
        if type(tweets_ids) is int:
            get_and_retweet_tweet(tweet_id=tweet_id)
        # Multiple tweets
        elif type(tweets_ids) is list:
            for tweet_id in tweets_ids:
                get_and_retweet_tweet(tweet_id=tweet_id)
        # Unknown type
        else:
            log.warn(f"Unknown parameter type received, {type(tweets_ids)} with content: <{tweets_ids}>")


    def find_keywords_routine(self, keywords: List[str]):
        """
        Routine for the FIND_KEYWORDS task
        Currently implemented as getting tweets from our timeline and "reading them".
        Whenever a tweet appears, we'll send a request to the control center asking if we should like/retweet them

        Parameters
        ----------
        keywords : `List[str]`
            List of keywords to search in the timeline tweets
        See Also
        --------
        read_timeline
        get_user_timeline_tweets
        """
        log.info("Starting Keywords Routine...")
        log.info("Getting Home Timeline")
        tweet_numbers = utils.random_between(settings.MIN_HOME_TIMELINE_TWEETS,
                                             settings.MAX_HOME_TIMELINE_TWEETS)
        log.info(f"Trying to get {tweet_numbers} tweets")
        timeline_posts = self.get_user_timeline_tweets(self.user,
                                                       count=tweet_numbers,
                                                       max_id=self.last_home_tweet)

        if not timeline_posts:
            log.info(f"No tweets found in timeline")
        else:
            log.info(f"Timeline has {len(timeline_posts)} tweets")
            log.info("'Reading' tweets in timeline")
            self.read_timeline(self.user, timeline_posts, keywords)
        log.info("Exiting Keywords Routine...")

    def follow_users_routine(self, params : Dict[str, Union[str,List[Union[str,int]]]]):
        """
        Routine for the FOLLOW_USERS task
        We can accept 2 types of users list, either by screen names or by IDs.
        Params is assumed to be this kind of structure

        "params" : {
            "type" : "screen_name"
            "data" : ["barackobama",...],
        }
        
        or 

        "params" : {
            "type" : "id"
            "data : [2312312312312,...],
        }

        Parameters
        ----------
        params : Dict[Any]
            Dictionary with the payload, the data itself + the type

        See Also
        --------
        search_in_user
        """
        log.info("Starting 'Follow Users' routine...")

        if not params["data"]:
            log.info("No users provided!")
        else:
            # To avoid having to write 2 loops, or making an if check on every loop,
            # we'll just take advantage of python's dict as params
            # So we'll kinda of do
            """
                fun_kwargs = {
                    params["type"] : value
                }
            """
            # By default, assume `user_ids`
            unclean_type = params["type"].lower()
            arg_type = "user_id"
            # making a check
            if unclean_type == "id" or unclean_type == "user_id":
                arg_type = "user_id"
            elif unclean_type == "screen_name":
                arg_type = "screen_name"

            for i in params["data"]:
                # get the user object
                # TODO: Use the cache as, you know, an actual cache
                log.info(f"Getting user object for User with ID={user_id}")
                arg_param = {
                    arg_type : i,
                }
                try:
                    user = self._api.get_user(*arg_param)
                    if user:
                        log.info(f"Found with: ", user)
                        self.search_in_user(user)
                except Exception as e:
                    log.error(f"Unable to find user by [{arg_type}] with <{i}>")
        log.info("Exiting Follow Users Routine...")

    def search_in_user(self, user_obj: User):
        """
        1. Sends the user object to the control center.
        2. Reads the user's description.
        3a. If the user is protected, tries to follow him and stop.
        3b. If he's not protected, then.
        4. Reads the user's timeline.
        5. Tries to follow the user.

        Parameters
        ----------
        user_obj : User
            User object
        """
        log.info(f"Searching User with id={user_obj.id}")
        # Save the user
        self._cache.save_user(user_obj)
        self.send_user(user_obj)
        # read the user's  description
        utils.read_text_and_wait(user_obj.description)
        if user_obj.protected:
            log.info(f"Found protected user with id={user_obj.id}")
            # just try to follow him, since we can't read his tweets
            try:
                user_obj.follow()
                log.info(f"Followed User with ID={user_obj.id}")
                self.send_event(MessageType.EVENT_USER_FOLLOWED, user_obj)
            except tweepy.error.TweepError as e:
                if e.api_code == 161:
                    # can't follow, just ignore
                    # TODO: implement logic for resuming follows
                    log.error(f"Unable to follow User with api_code={e.api_code},reason={e.reason}")
                else:
                    raise e
            return
        # he's not protected so try to check his timeline
        else:
            tweets_to_get = utils.random_between(settings.MIN_USER_TIMELINE_TWEETS,
                                                 settings.MAX_USER_TIMELINE_TWEETS)
            # get the user's timeline tweets
            tweets = self.get_user_timeline_tweets(user_obj, count=tweets_to_get)
            self.read_timeline(user_obj, tweets)
            try:
                user_obj.follow()
                log.info(f"Followed User with ID={user_obj.id}")
                self.send_event(MessageType.EVENT_USER_FOLLOWED, user_obj)
            except tweepy.error.TweepError as e:
                if e.api_code == 161:
                    log.error(f"Unable to follow User with SPECIAL api_code={e.api_code}")
                    pass
                else:
                    log.error(f"Unable to follow User with SPECIAL api_code={e.api_code}")
                    raise e
            return

    def get_user_timeline_tweets(self, user_obj: User, **kwargs) -> List[Tweet]:
        """
        Helper method so we don't have to worry about handling the home timeline

        Parameters
        ----------
        user_obj : `User`
            The User to get the tweets for
        kwargs : Dict[Any]
            Keyword arguments for the api
        Returns
        -------
        tweets: List[tweepy.models.Status]
            A List of tweets from the provided user's timeline
        """
        log.debug(f"Getting timeline tweets for User with id={user_obj.id}")
        if user_obj.id == self.user.id:
            return self._api.home_timeline()
        return user_obj.timeline(**kwargs)

    def read_timeline(self, user_obj: User, tweets: List[Tweet], keywords: List[str] = []):
        """
        Method for reading a user's tweets, from their timeline.
        For each tweet:
            If there are any keywords, then we do a simple verification of how many keywords from
            the tweet match, and ask the control center to like/retweet based on the percentage.
            If there are no keywords,  then ask the control center to like the tweet.

        Parameters
        ----------
        user_obj : User
            User object
        tweets : List[Tweet]
            List of Tweet objects
        keywords : List[str]
            Optional list of keywords.

        See Also
        --------
        find_keywords_routine
        search_in_user

        """
        log.debug(f"Reading User {user_obj}'s timeline")
        if not tweets:
            log.debug("No Tweets to read!")
            return

        last_tweet = tweets[0].id
        # Due to the nature of timelines, we need to pass user_obj for the logic regarding the jumps
        total_read_time = 0
        total_keywords = len(keywords)
        for tweet in tweets:
            if last_tweet < tweet.id:
                last_tweet = tweet.id
            log.debug(f"Saving Tweet with ID={tweet.id} to cache")
            # save the tweet
            self._cache.save_tweet(tweet)
            self.send_tweet(tweet)
            # read it's content
            total_read_time += utils.read_text_and_wait(tweet.text)
            # don't do anything if it's our own tweet
            if self.user.id == tweet.user.id:
                continue
            if not keywords:
                self.query_like_tweet(tweet)
                continue
            else:
                # For reading other timelines
                # if self.user.id != user_obj.id:
                # check for the keywords in the tweet
                keywords_tweet_matches = sum([1 for i in keywords if i in tweet.text])
                percentage_matches = keywords_tweet_matches / total_keywords
                # If at least a minimum matches
                if percentage_matches >= settings.MIN_KEYWORD_THRESHOLD:
                    # randomly decide to favourite
                    favourite_chance = utils.random_between(percentage_matches, 1)
                    log.debug(
                        f"Liking chance of «{favourite_chance}» out of «{settings.FAVOURITE_CHANCE}»")
                    if favourite_chance >= settings.FAVOURITE_CHANCE:
                        self.query_like_tweet(tweet)
                    # same for retweeting
                    retweet_chance = utils.random_between(percentage_matches, 1)
                    log.debug(
                        f"Retweeting chance of «{retweet_chance}» out of «{settings.RETWEET_CHANCE}»")
                    if retweet_chance >= settings.RETWEET_CHANCE:
                        self.query_retweet_tweet(tweet)
                # TODO: for reading our home timeline?
                # TODO: Do logic for replies

    def send_user(self, user: User) -> None:
        """
        Helper function for sending the user to the server

        Parameters
        ----------
        user : User
            The User Object to send
        """
        log.debug(f"Sending User object to: {self.data_exchange} with", user)
        payload = {
            "type"     : MessageType.SAVE_USER,
            "bot_id"   : self._id,
            "timestamp": utils.current_time(),
            "data"     : user.to_json(),
        }
        self.messaging.publish(vhost=self.vhost, xname=self.data_exchange,
                               rt_key=self.data_routing_key, payload=utils.to_json(payload))

    def send_tweet(self, tweet: Tweet):
        """
        Helper function for sending a tweet to the server

        Parameters
        ----------
        tweet : Tweet
            The Tweet Object to send
        """
        log.debug(f"Sending Tweet object to: {self.data_exchange} with", tweet)
        payload = {
            "type"     : MessageType.SAVE_TWEET,
            "bot_id"   : self._id,
            "timestamp": utils.current_time(),
            "data"     : tweet.to_json()
        }
        self.messaging.publish(vhost=self.vhost, xname=self.data_exchange,
                               rt_key=self.data_routing_key, payload=utils.to_json(payload))

    def send_query(self, messageType: MessageType, data: BaseModel):
        """
        Generic Helper function for sending a message to the server

        Parameters
        ----------
        messageType : MessageType
            The event to send
        data: BaseModel
            the data associated with the event (usually the object)
        """
        log.debug(f"Sending query <{messageType}> to: {self.query_exchange} with", data)
        payload = {
            "type"     : messageType,
            "bot_id"   : self._id,
            "timestamp": utils.current_time(),
            "data"     : data.to_json(),
        }
        self.messaging.publish(vhost=self.vhost, xname=self.query_exchange,
                               rt_key=self.query_routing_key, payload=utils.to_json(payload))

    def send_event(self, messageType: MessageType, data: BaseModel):
        """ Generic Helper function for sending an event to the server
        Parameters
        ----------
        messageType : `class` MessageType the event to send
        data: `class` BaseModel the data associated with the event (usually the object)
        """
        log.debug(f"Sending event <{messageType}> to: {self.log_exchange} with", data)
        payload = {
            "type"     : messageType,
            "bot_id"   : self._id,
            "timestamp": utils.current_time(),
            "data"     : data.to_json(),
        }
        self.messaging.publish(vhost=self.vhost, xname=self.log_exchange,
                               rt_key=self.log_routing_key, payload=utils.to_json(payload))

    def query_like_tweet(self, tweet: Tweet):
        """
            Method for asking the control center asking whether to like a tweet.
        """
        if tweet.favorited:
            log.info(f"Tweet with ID={tweet.id} already liked, no need to like again")
            return
        else:
            log.info(f"Asking to like Tweet with ID={tweet.id}")
            self.send_query(MessageType.QUERY_TWEET_LIKE, tweet)

    def query_retweet_tweet(self, tweet: Tweet):
        """
            Method for asking the control center asking whether to retweet a tweet.
        """
        if tweet.retweeted:
            log.info(f"Tweet with ID={tweet.id} already retweeted, no need to retweet again")
            return
        else:
            log.info(f"Asking to Retweet Tweet with ID={tweet.id}")
            self.send_query(MessageType.QUERY_TWEET_RETWEET, tweet)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_agent",
                        help="User Agent to use. Defaults to the one present in settings.py",
                        default=os.environ.get("USER_AGENT", settings.DEFAULT_USER_AGENT))
    parser.add_argument("--tor_proxy",
                        help="HTTPS Proxy (to use with TOR)",
                        default=os.environ.get("TOR_PROXY", ""))
    parser.add_argument("--server_host",
                        help="Location of the server to connect to. Defaults to 127.0.0.1",
                        default=os.environ.get("SERVER_HOST", "127.0.0.1"))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    proxies = args.tor_proxy
    user_agent = args.user_agent
    server = args.server_host
    key = os.environ["KEY"]
    secret = os.environ["SECRET"]
    token = os.environ["TOKEN"]
    token_secret = os.environ["TOKEN_SECRET"]
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
    log.addHandler(handler)
    # TODO: change password
    messaging_manager = Client(api_url=server,
                               user='pi_rabbit_admin',
                               passwd='yPvawEVxks7MLg3lfr3g')

    wrapper_api = TweepyWrapper(tor_proxies=proxies, user_agent=user_agent, consumer_key=key,
                                consumer_secret=secret, token=token, token_secret=token_secret)

    bot = TwitterBot(bot_id=token.split('-')[0], messaging_manager=messaging_manager,
                     api=wrapper_api)
    bot.run()
    exit(0)
