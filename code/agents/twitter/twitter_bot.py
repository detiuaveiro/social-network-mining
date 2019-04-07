import argparse
import logging
import os
import sys
from typing import List, Any, Callable, Optional

import tweepy

import settings
import utils
from cache import Cache
from models import User

log = logging.getLogger("bot-agents")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)


class TwitterBot:
    def __init__(self, *, consumer_key: str, consumer_secret: str, token: str, token_secret: str,
                 user_agent: str,
                 tor_proxies: str = ""):
        self.user_agent = user_agent
        self.user: User
        self.keywords: List[str]
        self._proxies = tor_proxies
        self._id = token.split("-")[0]
        self.keywords = ["governo"]
        self._cache: Cache = Cache(f"cache_{self._id}", logger=log)
        self.key = consumer_key
        self.token = token
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(token, token_secret)
        self._api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, proxy=self._proxies)
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
        # Wrapper for Tweet
        # TODO
        elif data_type == tweepy.models.Status:
            return dirty_data
        # List of something
        elif data_type == list or data_type == tweepy.models.ResultSet:
            # if there's any elements
            if dirty_data:
                # check the type of the first
                first_type = type(dirty_data[0])
                if first_type == tweepy.models.User:
                    return [User.from_json(self._api, u._json) for u in dirty_data]
        # edge case, return data
        return dirty_data

    def run(self):
        # Initial  setup doesn't count towards run time
        self._setup()
        self.start()
        # TODO: Fix writing to file issue
        ## Start the process and run until limit is reached
        # p = multiprocessing.Process(target=self.start, name="<TwitterBot id={self.id}>")
        # p.start()
        # p.join(utils.random_between(settings.MIN_RUN_TIME, settings.MAX_RUN_TIME))

    def _setup(self):
        log.debug(f"Setting up with: {self}")
        log.debug("Opening Cache")
        # Open the cache
        self._cache.open()

        log.debug("Verifying credentials")
        # TODO: make sure we received data?
        self.user: User = self._request(self._api.verify_credentials)
        log.debug(f"Logged in as:{self.user}")
        # make request to the server
        # TODO: Authenticate
        res = None
        # saving our user obj in the cache
        self._cache.save_user(self.user)
        # if it's our first time, then we need to setup our routine
        if res is None:
            log.debug("First time detected. Starting first time routine...")
            self.find_new_suggestions()
        # TODO: Do some cleaning?
        # Otherwise, just keep moving
        else:
            return

    def find_new_suggestions(self):
        log.debug(f"Finding new suggestions with keywords={self.keywords}")
        # see if we got any keywords
        if not self.keywords:
            log.error("No keywords provided!")
            return
        # find new users
        new_users = self._request(self._api.search_users, self.keywords)

        for user in new_users:
            self.search_in_user(user)

    def search_in_user(self, user_obj: User):
        log.debug(f"Searching User with id={user_obj.id}")
        # only search if it's not us
        if self.user.id == user_obj.id:
            return

        # Save the user
        self._cache.save_user(user_obj)

        # Check if we're following him
        if not user_obj.following:
            # read the user's  description
            utils.read_text_and_wait(user_obj.description)
            if user_obj.protected:
                log.debug(f"Found protected user with id={user_obj.id}")
                # just try to follow him, since we can't read his tweets
                try:
                    user_obj.follow()
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
                last_read_tweet = self.read_timeline(user_obj, tweets)
                # TODO: implement logic for following user?
                try:
                    user_obj.follow()
                except tweepy.error.TweepError as e:
                    if e.api_code == 161:
                        # can't follow, just ignore
                        # TODO: implement logic for resuming follows
                        pass
                    else:
                        raise e
                return

    def get_user_timeline_tweets(self, user_obj: User, **kwargs) -> List[tweepy.models.Status]:
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

    def read_timeline(self, user_obj, tweets: List[tweepy.models.Status]) -> Optional[None]:
        log.debug(f"Reading User {user_obj}'s timeline")
        if not tweets:
            return
        last_tweet = tweets[0].id
        # Due to the nature of timelines, we need to pass user_obj for the logic regarding the jumps
        total_read_time = 0
        total_keywords = len(self.keywords)
        for tweet in tweets:
            if last_tweet < tweet.id:
                last_tweet = tweet.id
            log.debug(f"Saving Tweet with ID={tweet.id}")
            # save the tweet
            self._cache.save_tweet(tweet)
            # read it's content
            total_read_time += utils.read_text_and_wait(tweet.text)
            # don't do anything if it's our own tweet
            if self.user.id == tweet.user.id:
                continue
            # TODO: Probably not acceptable behaviour but, if we're not provided any keywords, we'll like everything
            if total_keywords == 0:
                # TODO: replace with proper wrapping
                log.debug(f"Liking Tweet with ID={tweet.id}")
                self._request(self._api.create_favorite, tweet.id)
                continue
            else:
                # For reading other timelines
                # if self.user.id != user_obj.id:
                # check for the keywords in the tweet
                keywords_tweet_matches = sum([1 for i in self.keywords if i in tweet.text])
                percentage_matches = keywords_tweet_matches / total_keywords
                # If at least a minimum matches
                if percentage_matches >= settings.MIN_KEYWORD_THRESHOLD:
                    # randomly decide to favourite
                    favourite_chance = utils.random_between(percentage_matches, 1)
                    log.debug(
                        f"Liking chance of «{favourite_chance}» out of «{settings.FAVOURITE_CHANCE}»")
                    if favourite_chance >= settings.FAVOURITE_CHANCE:
                        log.debug(f"Liking Tweet with ID={tweet.id}")
                        self._request(self._api.create_favorite, tweet.id)
                    # same for retweeting   
                    retweet_chance = utils.random_between(percentage_matches, 1)
                    log.debug(
                        f"Retweeting chance of «{retweet_chance}» out of «{settings.RETWEET_CHANCE}»")
                    if retweet_chance >= settings.RETWEET_CHANCE:
                        log.debug(f"Retweeting Tweet with ID={tweet.id}")
                        self._request(self._api.retweet, tweet.id)
                # TODO: for reading our home timeline
                # 
        return last_tweet

    def start(self):
        log.debug("Starting Routine...")
        log.debug("Getting Timeline")
        tweet_numbers = utils.random_between(settings.MIN_HOME_TIMELINE_TWEETS,
                                             settings.MAX_HOME_TIMELINE_TWEETS)
        log.debug(f"Trying to get {tweet_numbers} tweets")
        last_home_tweet = self._cache.get("last_home_tweet")
        timeline_posts: List[tweepy.models.Status]
        if last_home_tweet:
            log.debug(f"Last Tweet read has id={last_home_tweet}")
            timeline_posts = self.get_user_timeline_tweets(self.user, count=tweet_numbers,
                                                           max_id=last_home_tweet)
        else:
            log.debug(f"No Last tweets found")
            timeline_posts = self.get_user_timeline_tweets(self.user, count=tweet_numbers)
        if not timeline_posts:
            log.debug(f"No tweets found in timeline")
        else:
            log.debug(f"Timeline has {len(timeline_posts)} tweets")
            log.debug("'Reading' tweets in timeline")
            last_home_tweet = self.read_timeline(self.user, timeline_posts)
            self._cache.set("last_home_tweet", last_home_tweet)
        log.debug("Find new users?")
        new_suggestions_chance = utils.random_between(0, 1)
        if new_suggestions_chance >= settings.FIND_NEW_SUGGESTIONS_CHANCE:
            log.debug(f"Finding new users with chance={new_suggestions_chance}")
            self.find_new_suggestions()
        # TODO: Send Tweets to Server
        log.debug("Closing Cache")
        self._cache.close()
        log.debug("Exiting...")


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
    bot = TwitterBot(tor_proxies=proxies, user_agent=user_agent, consumer_key=key,
                     consumer_secret=secret, token=token, token_secret=token_secret)
    bot.run()
    exit(0)
