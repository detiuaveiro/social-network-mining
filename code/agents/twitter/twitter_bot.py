import argparse
from typing import List, Dict, Any, Callable, Optional
import logging
import tweepy
import os
import readtime
import sys
import time
from models import User
import settings
import utils

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
        self._id = token.split(";")
        self.key = consumer_key
        self.token = token
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(token, token_secret)
        self._api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, proxy=self._proxies)

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
        # TODO: make a check for dynamic attribute of _json
        if dirty_data:
            return dirty_data._json
        return None

    def run(self):
        self._setup()
        self.start()

    def _setup(self):
        log.debug(f"Setting up with: {self}")
        log.debug("Verifying credentials")
        # TODO: make sure we received data?
        data = self._request(self._api.verify_credentials)
        self.user = User.from_json(self._api, data)
        log.debug("Logged in as:\n"
                  f"ID: {self.user.id}\n"
                  f"Username: {self.user.screen_name}\n")
        # make request to the server
        # TODO: Authenticate
        res = 0
        # if it's our first time, then we need to setup our routine
        if res is None:
            self._first_time_setup()
        # TODO: Do some cleaning?
        # Otherwise, just keep moving
        else:
            return

    def _first_time_setup(self):
        log.debug("First time detected. Starting first time routine...")
        # first time we're executing, so first we see if we got provided any keywords
        pass

    def read_timeline(self, tweets: List[tweepy.models.Status]) -> Optional[None]:
        total_read_time = 0
        for tweet in tweets:
            time_for_tweet = readtime.of_text(tweet.text)
            # just in case the text was empty
            # TODO: Do proper time for entities, etc
            time_for_tweet = time_for_tweet if time_for_tweet > 1 else 1
            # wait for the some time
            wait_time = utils.random_between(time_for_tweet * 0.9, time_for_tweet * 1.10)
            total_read_time += wait_time
            time.sleep(wait_time)
            # TODO: do logic for like/retweet

    def start(self):
        log.debug("Starting Routine...")
        log.debug("Getting Timeline")
        timeline_posts: List[tweepy.models.Status] = self._request(self._api.home_timeline)
        log.debug(f"Timeline has {len(timeline_posts)} tweets")
        log.debug("'Reading' tweets in timeline")
        self.read_timeline(timeline_posts)
        # TODO: Send Tweets to Server


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
