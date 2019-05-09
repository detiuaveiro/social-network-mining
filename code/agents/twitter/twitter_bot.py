import argparse
import logging
import os
import sys
from typing import List, Any, Callable, Optional, Dict

import tweepy
from pyrabbit2 import Client

import settings
import utils
from cache import Cache
from enums import Task, MessageType
from exceptions import NoMessagesInQueue
from models import User, Tweet, BaseModel

log = logging.getLogger("bot-agents")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)


class TwitterBot:
    def __init__(self, messaging_manager: Client, *, consumer_key: str,
                 consumer_secret: str,
                 token: str, token_secret: str,
                 user_agent: str,
                 tor_proxies: str = ""):
        self.messaging = messaging_manager
        self.user_agent = user_agent
        self.user: User
        self._proxies = tor_proxies
        self._id = token.split("-")[0]
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
        self.key: str = consumer_key
        self.token: str = token
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(token, token_secret)
        self._api: tweepy.API = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                                           proxy=self._proxies)
        # no comments
        self._api.create_favourite = self._api.create_favorite

    def __repr__(self):
        return f"<TwitterBot id={self._id}, user_agent={self.user_agent}, proxies={self._proxies}, key={self.key}, token={self.token}>"

    def _request(self, fun: Callable, *args, **kwargs) -> Optional[Any]:
        """
        Wrapper method so we don't have to write the kwargs on every api call
        Parameters
        ----------
        fun : function
            The api callback
        args : List[Any]
            Arguments to the function
        kwargs :

        Returns
        -------
        data: dict
            A JSON response, depending on the function called
        """
        kwargs["headers"] = {
            'User-Agent': self.user_agent,
        }
        log.debug(f"Making Request to {fun.__name__}\n")
        # Since we're making our own version of the models, we're going to ignore everything except the json
        dirty_data = fun(*args, **kwargs)

        # Wrapper for User
        data_type = type(dirty_data)
        if data_type == tweepy.models.User:
            return User.from_json(self._api, dirty_data._json)
        elif data_type == tweepy.models.Status:
            return Tweet.from_json(self._api, dirty_data._json)
        # List of something
        elif data_type == list or data_type == tweepy.models.ResultSet:
            # if there's any elements
            if dirty_data:
                # check the type of the first
                first_type = type(dirty_data[0])
                if first_type == tweepy.models.User:
                    return [User.from_json(self._api, u._json) for u in dirty_data]
                elif first_type == tweepy.models.Status:
                    return [Tweet.from_json(self._api, u._json) for u in dirty_data]
        # edge case, return data
        return dirty_data

    def _setup_messaging(self):
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
        log.debug(f"Setting up with: {self}")
        log.debug("---------------------------------------")
        self._setup_messaging()
        log.debug("Verifying credentials")
        self.user: User = self._request(self._api.verify_credentials)
        log.debug(f"Logged in as:{self.user}")
        log.debug(f"Sending our user to {self.data_exchange}")
        self.send_user(user=self.user)

        log.debug("Opening Cache")
        self._cache.open()
        log.debug("Checking last Tweet")
        self.last_home_tweet = self._cache.get("last_home_tweet", None)
        log.debug(f"Last Tweet was: <{self.last_home_tweet}>")

    def get_new_message(self):
        msg: List[Dict] = self.messaging.get_messages(vhost=self.vhost, qname=self.tasks_queue,
                                                      count=1)
        if msg and msg[0].get("payload", None):
            return msg[0]["payload"]
        raise NoMessagesInQueue("Queue has no messages left!")

    def run(self):
        self._setup()
        retries = settings.MAX_RETRIES
        log.debug("Starting to get tasks...")
        while True:
            try:
                log.debug(f"Getting next task from {self.tasks_queue}")
                task_msg = self.get_new_message()
                task_type, task_params = task_msg["type"], task_msg["params"]
                log.debug(f"Received task {task_msg} with:", task_params)
                if task_msg == Task.FIND_BY_KEYWORDS:
                    self.find_keywords_routine(task_params["keywords"])
                    pass
                elif task_msg == Task.FOLLOW_USERS:
                    self.follow_users_routine(task_params["users"])
                    pass
                elif task_msg == Task.LIKE_TWEETS:
                    self.like_tweets_routine(task_params["tweets"])
                elif task_msg == Task.RETWEET_TWEETS:
                    self.retweet_tweets_routine(task_params["tweets"])
                else:
                    log.warning(f"Received unknown task_msg: {task_msg}")
            except NoMessagesInQueue:
                if retries == 0:
                    break
                log.debug("No Messages found. Waiting...")
                utils.wait_for(5)
                retries -= 1
        self.cleanup()

    def cleanup(self):
        log.warning("TODO: Implement Clean up")
        self._cache.close()

    def like_tweets_routine(self, tweets):
        log.debug("Starting 'Like Tweets' routine...")
        for tweet_id in tweets:
            tweet: Tweet = self._request(self._api.get_status, tweet_id=tweet_id)
            if tweet.favorited:
                log.debug(f"Tweet with ID={tweet.id} already liked, no need to like again")
            else:
                log.debug(f"Liking Tweet with ID={tweet.id}")
                tweet.like()
                self.send_event(MessageType.EVENT_TWEET_LIKED, tweet)

    def retweet_tweets_routine(self, tweets):
        log.debug("Starting 'Retweet Tweets' routine...")
        for tweet_id in tweets:
            tweet: Tweet = self._request(self._api.get_status, tweet_id=tweet_id)
            if tweet.retweeted:
                log.debug(f"Tweet with ID={tweet.id} already retweeted, no need to retweet again")
            else:
                log.debug(f"Retweeting Tweet with ID={tweet.id}")
                tweet.retweet()
                self.send_event(MessageType.EVENT_TWEET_RETWEETED, tweet)

    def find_keywords_routine(self, keywords):
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

    def follow_users_routine(self, users: List[int]):
        log.info("Starting 'Follow Users' routine...")
        if not users:
            log.info("No users provided!")
        else:
            for user_id in users:
                # Skip our own, just in case
                if user_id == self.user.id:
                    continue
                # get the user object
                # TODO: Use the cache as, you know, an actual cache
                log.info(f"Getting user object for User with ID={user_id}")
                user = self._request(self._api.get_user, user_id=user_id)
                log.info(f"Found with: ", user)
                self.search_in_user(user)
        log.info("Exiting Follow Users Routine...")

    def send_user(self, user: User) -> None:
        """ Helper function for sending the user to the server
        Parameters
        ----------
        user : `class` User
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
        """ Helper function for sending a tweet to the server
        Parameters
        ----------
        tweet : `class` Tweet
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
        """ Generic Helper function for sending an to the server
        Parameters
        ----------
        messageType : `class` MessageType the event to send
        data: `class` BaseModel the data associated with the event (usually the object)
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
        if tweet.favorited:
            log.info(f"Tweet with ID={tweet.id} already liked, no need to like again")
            return
        else:
            log.info(f"Asking to like Tweet with ID={tweet.id}")
            self.send_query(MessageType.QUERY_TWEET_LIKE, tweet)

    def query_retweet_tweet(self, tweet: Tweet):
        if tweet.retweeted:
            log.info(f"Tweet with ID={tweet.id} already retweeted, no need to retweet again")
            return
        else:
            log.info(f"Asking to Retweet Tweet with ID={tweet.id}")
            self.send_query(MessageType.QUERY_TWEET_RETWEET, tweet)

    def search_in_user(self, user_obj: User):
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
                    pass
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
        log.debug(f"Getting timeline tweets for User with id={user_obj.id}")
        """
        Helper method so we don't have to worry about handling the home timeline
        ----------
        usr : User
            The User to get the tweets for
        kwargs : Dict[Any]
            Keyword arguments for the api
        Returns
        -------
        tweets: List[tweepy.models.Status]
            A List of tweets from the provided user's timeline
        """
        if user_obj.id == self.user.id:
            return self._request(self._api.home_timeline, **kwargs)
        return user_obj.timeline(**kwargs)

    def read_timeline(self, user_obj, tweets: List[Tweet], keywords=[]):
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

    # TODO: change password
    messaging_manager = Client(api_url=server,
                               user='pi_rabbit_admin',
                               passwd='yPvawEVxks7MLg3lfr3g')

    bot = TwitterBot(messaging_manager,
                     tor_proxies=proxies, user_agent=user_agent, consumer_key=key,
                     consumer_secret=secret, token=token, token_secret=token_secret)
    bot.run()
    exit(0)
