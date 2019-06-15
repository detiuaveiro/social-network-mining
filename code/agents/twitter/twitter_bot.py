import argparse
import logging
import os
import sys
from typing import List, Dict, Union

import pyrabbit2
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


def reconnect_messagging(_func=None, *, max_times=5):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            for current_reconnect in range(max_times):
                try:
                    return func(self, *args, **kwargs)
                except pyrabbit2.http.NetworkError as e:
                    log.error("Unable to retrieve a message. Retrying...")
                    # if we reach the maximum number of retries, just end the program
                    # In theory, this shouldn't happen
                    if current_reconnect == max_times:
                        raise e
                    # recreate the instance
                    self.messaging = Client(api_url=os.environ.get("SERVER_HOST", "127.0.0.1"),
                                            user=settings.RABBIT_USERNAME,
                                            passwd=settings.RABBIT_PASSWORD)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def log_account_suspended(_func=None, **d_kwargs):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except tweepy.error.TweepError as e:
                # Log the error
                log.warning(f"TweepyError with code=<{e.api_code}> and reason=<{e.reason}>, {e}")
                # if it was an error code of account suspended, send a log
                if e.api_code == 63 or e.api_code == 64 or e.api_code == 326:
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

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


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

    @reconnect_messagging(max_times=settings.MAX_RABBIT_RETRIES)
    def _setup_messaging(self):
        """
            Private method for setuping the messaging connections
        """
        log.debug("Setting up Messaging to: Receive Tasks")
        log.debug(f"Connecting to exchange {self.tasks_exchange}")
        self.messaging.create_exchange(vhost=self.vhost, name=self.tasks_exchange, xtype="direct")
        log.debug(f"Creating queue {self.tasks_queue}")
        self.messaging.create_queue(vhost=self.vhost, name=self.tasks_queue, durable=True)
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

    @log_account_suspended
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
        log.info("Reading Home Timeline")
        self.read_timeline(self.user, jump_users=False)
        log.info("Checking Direct Messages")
        self.check_direct_messages()
        # log.debug("Checking last Tweet")
        # self.last_home_tweet = self._cache.get("last_home_tweet", None)
        # log.debug(f"Last Tweet was: <{self.last_home_tweet}>")

    @reconnect_messagging(max_times=settings.MAX_RABBIT_RETRIES)
    def get_new_message(self):
        """
            Helper message to get a new message from the tasks queue
        """
        msg: List[Dict] = self.messaging.get_messages(vhost=self.vhost, qname=self.tasks_queue,
                                                      count=1)
        if msg and msg[0].get("payload", None):
            return utils.from_json(msg[0]["payload"])
        raise NoMessagesInQueue("Queue has no messages left!")

    @log_account_suspended
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
                log.debug(f"Received task {task_msg} with: {task_params}")
                if task_type == Task.FIND_BY_KEYWORDS:
                    log.warning(f"Not processing {Task.FIND_BY_KEYWORDS.name} with {task_params}")
                elif task_type == Task.FOLLOW_USERS:
                    self.follow_users_routine(task_params)
                elif task_type == Task.LIKE_TWEETS:
                    self.like_tweets_routine(task_params)
                elif task_type == Task.RETWEET_TWEETS:
                    self.retweet_tweets_routine(task_params)
                elif task_type == Task.FIND_FOLLOWERS:
                    self.find_followers(task_params)
                elif task_type == Task.POST_TWEET:
                    self.post_tweet_routine(task_params)
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
        """
        Method for cleaning up any connections.
        TODO: maybe remove this?
        """
        log.warning("TODO: Implement Clean up")
        self._cache.close()

    def check_direct_messages(self):
        messages_list = self._api.direct_messages()
        self.send_data(messages_list, message_type=MessageType.SAVE_DIRECT_MESSAGES)

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
            read_time = utils.read_text_and_wait(tweet.text)
            log.debug(f"Read Tweet in {read_time}")
            if tweet.favorited:
                log.debug(f"Tweet with ID={tweet.id} already liked, no need to like again")
            else:
                log.debug(f"Liking Tweet with ID={tweet.id}")
                tweet.like()
                self.send_event(MessageType.EVENT_TWEET_LIKED, tweet)

        # Single tweet
        if type(tweets_ids) is int:
            get_and_like_tweet(tweet_id=tweets_ids)
        # Multiple tweets
        elif type(tweets_ids) is list:
            for tweet_id in tweets_ids:
                get_and_like_tweet(tweet_id=tweet_id)
        # Unknown type
        else:
            log.warning(
                f"Unknown parameter type received, {type(tweets_ids)} with content: <{tweets_ids}>")

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
            read_time = utils.read_text_and_wait(tweet.text)
            log.debug(f"Read Tweet in {read_time}")
            if tweet.retweeted:
                log.debug(f"Tweet with ID={tweet.id} already retweeted, no need to retweet again")
            else:
                log.debug(f"Retweeting Tweet with ID={tweet.id}")
                tweet.retweet()
                self.send_event(MessageType.EVENT_TWEET_RETWEETED, tweet)

        # Single tweet
        if type(tweets_ids) is int:
            get_and_retweet_tweet(tweet_id=tweets_ids)
        # Multiple tweets
        elif type(tweets_ids) is list:
            for tweet_id in tweets_ids:
                get_and_retweet_tweet(tweet_id=tweet_id)
        # Unknown type
        else:
            log.warning(
                f"Unknown parameter type received, {type(tweets_ids)} with content: <{tweets_ids}>")

    def post_tweet_routine(self, data: dict):
        log.debug("Starting Post Tweet Routine")
        reply_id = data.get("in_reply_to_status_id", None)
        status = data.get("status", None)
        if not status:
            log.warning("No status providing! Ignoring")
            return
        # "Simulating" some kind of posting a tweet by "writing it"
        # On average, a person reads 2 to 3 times faster than they type
        # So if we just "read" the text 3 times, we're more or less waiting the same time as
        # if we were typing it
        write_time = utils.read_text_and_wait(status * 3)
        log.debug(f"'Wrote' Tweet in {write_time}")
        tweet_sent = None
        if reply_id is None:
            tweet_sent = self._api.update_status(status=status,
                                                 auto_populate_reply_metadata=True)
        else:
            tweet_sent = self._api.update_status(status=status,
                                                 auto_populate_reply_metadata=True,
                                                 in_reply_to_status_id=reply_id)
        if tweet_sent:
            self.send_tweet(tweet_sent)

    def find_followers(self, params: Dict[str, Union[str, List[Union[str, int]]]]):
        """
        Routine for the FIND_FOLLOWERS task
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
        """

        log.info("Starting 'Find Followers' routine...")

        if not params["data"]:
            log.info("No users provided!")
        else:
            # By default, assume `user_ids`
            unclean_type = params["type"].lower()
            arg_type = "user_id"
            # making a check
            if unclean_type == "id" or unclean_type == "user_id":
                arg_type = "user_id"
            elif unclean_type == "screen_name":
                arg_type = "screen_name"

            # To minimize the impact of people changing their screen_names, we're going to try and get their user objects
            user_obj_ids = []
            for param in params["data"]:
                log.info(f"Getting user object for User by [{arg_type}] with <{param}>")
                arg_param = {
                    arg_type: param,
                }
                user = None
                try:
                    user = self._api.get_user(**arg_param)
                except tweepy.error.TweepError as e:
                    log.error(f"Unable to find user by [{arg_type}] with <{param}>, due to {e}")
                if user:
                    self.send_user(user)
                    user_obj_ids += [user.id]
            if not user_obj_ids:
                log.warning(
                    "Could not find any of the Users Objects! Not searching for their Followers")
            # will be skipped if warning above is done
            # Since we already got their user objects, might as well send and use IDs all over
            for user_id in user_obj_ids:
                log.info(f"Getting Followers for User with ID <{user_id}>")
                try:
                    followers = self._api.followers_ids(id=user_id)
                    if followers:
                        # if they have followers, we need to send the user objects of the followers
                        # and then the followers list
                        # NOTE: Twitter API limits to 100 followers per request
                        for follower_id in range(0, len(followers), 100):
                            try:
                                user_objects = self._api.lookup_users(
                                    user_ids=followers[follower_id:follower_id + 100])
                                # sending the users
                                for user in user_objects:
                                    self.send_user(user)
                            except tweepy.error.TweepError as e:
                                log.error(
                                    f"Unable to get follower[{follower_id}:{follower_id + 100}]' objects for User {user_id}, with reason {e.reason}")
                                # utils.wait_for(5)
                        # after sending each user object (hopefully), send the followers
                        self.send_data({user_id: followers}, MessageType.SAVE_FOLLOWERS)
                except tweepy.error.TweepError as e:
                    log.error(
                        f"Unable to find Followers for User with ID <{param}> because reason={e.reason}")
        log.info("Exiting Follow Users Routine...")

    def follow_users_routine(self, params: Dict[str, Union[str, List[Union[str, int]]]]):
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
                log.info(f"Getting user object for User by [{arg_type}] with <{i}>")
                arg_param = {
                    arg_type: i,
                }
                user = None
                try:
                    user = self._api.get_user(**arg_param)
                except tweepy.error.TweepError as e:
                    log.error(f"Unable to find user by [{arg_type}] with <{i}> due to {e}")
                if user:
                    log.info(f"Found with: {user}")
                    self.search_in_user(user)
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

        # self._cache.save_user(user_obj)
        # Save the user
        self.send_user(user_obj)
        # If we're not following him, try to follow him
        if not user_obj.following:
            # read the user's  description
            utils.read_text_and_wait(user_obj.description)
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
                    log.error(f"Error with api_code={e.api_code},reason={e.reason}")
        # If the user isn't protected or he's protected and we're following him, read his timeline
        if not user_obj.protected or (user_obj.protected and user_obj.following):
            self.read_timeline(user_obj, jump_users=True)

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
        tweets: List[Tweet]
            A List of tweets from the provided user's timeline
        """
        log.debug(f"Getting timeline tweets for User with id={user_obj.id}")
        if user_obj.id == self.user.id:
            return self._api.home_timeline()
        return user_obj.timeline(**kwargs)

    def read_timeline(self, user_obj: User, *, jump_users=False,
                      max_depth=3, max_jumps=5, current_depth=0, total_jumps=0):
        """
        Method for reading a user's timeline.
        It jumps between timelines with a recursive call of this function

        Parameters
        ----------
        user_obj : User
            User object to read the timeline for
        jump_users : bool
            Flag to know if we should jump between user's tweets or not
        max_depth : int
            Max depth to jump
        max_jumps : int
            Max number of total jumps to do
        current_depth : int
            Internal control variable for recursive return
        total_jumps : int
            Internal variable for recursive return
        """
        log.debug(f"Reading User {user_obj}'s timeline")
        tweets_to_get = utils.random_between(settings.MIN_USER_TIMELINE_TWEETS,
                                             settings.MAX_USER_TIMELINE_TWEETS)
        # get the user's timeline tweets
        tweets = self.get_user_timeline_tweets(user_obj, count=tweets_to_get)
        if not tweets:
            log.debug("No Tweets to read!")
            return

        total_read_time = 0
        for tweet in tweets:
            # log.debug(f"Saving Tweet with ID={tweet.id} to cache")
            # save the tweet
            # self._cache.save_tweet(tweet)
            self.send_tweet(tweet)

            # read it's content
            total_read_time += utils.read_text_and_wait(tweet.text)
            # If it's our own tweet, we don't really need to do any logic
            if self.user.id == tweet.user.id:
                continue
            # Processing the tweet regarding liking/retweeting
            if not tweet.favorited:
                self.query_like_tweet(tweet)
            if not tweet.retweeted:
                self.query_retweet_tweet(tweet)
            # If the author of the tweet isn't the same user that we're reading the timeline
            # (Because retweets can appear), then jump and do the logic for reading the timeline
            # (assuming we haven't reached max jumps)
            if (not jump_users) or (total_jumps == max_jumps) or (current_depth == max_depth):
                continue
            elif tweet.user.id != user_obj.id:
                # save the user
                self.send_user(tweet.user)
                if tweet.user.protected and not tweet.user.following:
                    log.warning(
                        f"Found user with ID={tweet.user.id} but he's protected and we're not following him, so can't read his timeline")
                    continue
                elif tweet.user.suspended:
                    log.warning(
                        f"Found user with ID={tweet.user.id} but his account was suspended, so can't read his timeline")
                    continue
                else:
                    self.read_timeline(user_obj,
                                   jump_users=jump_users,
                                   total_jumps=total_jumps + 1,
                                   max_jumps=max_jumps,
                                   current_depth=current_depth + 1,
                                   max_depth=max_depth, )

        log.debug(f"Read {user_obj}'s timeline in {total_read_time} seconds")

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

    def send_user(self, user: User) -> None:
        """
        Helper function for sending the user to the server

        Parameters
        ----------
        user : User
            The User Object to send
        """
        log.debug(f"Sending {user}")
        self.send_data(user.to_json(), MessageType.SAVE_USER)

    def send_tweet(self, tweet: Tweet):
        """
        Helper function for sending a tweet to the server

        Parameters
        ----------
        tweet : Tweet
            The Tweet Object to send
        """
        log.debug(f"Sending {tweet}")
        self.send_data(tweet.to_json(), MessageType.SAVE_TWEET)

    def send_data(self, data, message_type: MessageType):
        self._send_message(data, message_type=message_type,
                           routing_key=self.data_routing_key,
                           exchange=self.data_exchange)

    def send_query(self, message_type: MessageType, data: BaseModel):
        """
        Generic Helper function for sending a query to the server

        Parameters
        ----------
        message_type : MessageType
            The query to send
        data: BaseModel
            the data associated with the event (usually the object)
        """
        log.debug(f"Sending {data}")
        self._send_message(data.to_json(), message_type=message_type,
                           routing_key=self.query_routing_key,
                           exchange=self.query_exchange)

    def send_event(self, message_type: MessageType, data: BaseModel):

        """ Generic Helper function for sending an event to the server
        Parameters
        ----------
        message_type : MessageType
            the event to send
        data: BaseModel
            the data associated with the event (usually the object)
        """
        log.debug(f"Sending {data}")
        self._send_message(data.to_json(), message_type=message_type,
                           routing_key=self.log_routing_key,
                           exchange=self.log_exchange)

    @reconnect_messagging(max_times=settings.MAX_RABBIT_RETRIES)
    def _send_message(self, data, *, message_type: MessageType, routing_key: str, exchange: str):
        log.debug(
            f"Sending <{message_type.name}> to exchange [{exchange}] with routing_key [{routing_key}]")
        payload = utils.wrap_message(data, bot_id=self._id, message_type=message_type)
        self.messaging.publish(vhost=self.vhost, xname=exchange, rt_key=routing_key,
                               payload=utils.to_json(payload))


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
    handler.setFormatter(
        logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
    log.addHandler(handler)
    # TODO: change password
    messaging_manager = Client(api_url=server,
                               user=settings.RABBIT_USERNAME,
                               passwd=settings.RABBIT_PASSWORD)

    wrapper_api = TweepyWrapper(tor_proxies=proxies, user_agent=user_agent, consumer_key=key,
                                consumer_secret=secret, token=token, token_secret=token_secret)

    bot = TwitterBot(bot_id=token.split('-')[0], messaging_manager=messaging_manager,
                     api=wrapper_api)
    bot.run()
    exit(0)
