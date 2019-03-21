from typing import List
import time
import tweepy
import settings
from api import TweepyWrapper

from interfaces import Bot
from models import Tweet, User
from utils import random_delay


class TwitterBot(Bot):

    def __init__(self, **options):
        self._closed = False
        self._user_agent = options.pop("user_agent")
        self._proxy = options.pop("tor_proxy", None)
        self._api: TweepyWrapper = None

    def connect_to_api(self, **kwargs):
        auth = tweepy.OAuthHandler(kwargs.pop("consumer_key"), kwargs.pop("consumer_secret"))
        auth.set_access_token(kwargs.pop("access_token"), kwargs.pop("access_token_secret"))
        self._api = TweepyWrapper(auth_handler=auth, wait_on_rate_limit=True, proxy=self._proxy)

    def start(self, **kwargs):
        db_settings = kwargs.pop("database")
        self.connect_to_storage(**db_settings)
        api_settings = kwargs.pop("api")
        self.connect_to_api(**api_settings)

    def get_tasks(self, state=None):
        """
        """

        return [self.get_timeline]

    def run(self):
        while not self._closed:
            tasks = self.get_tasks()
            for task in tasks:
                ret = task()
                time.sleep(
                    random_delay(settings.MIN_WAIT_TIME_PER_TASK, settings.MAX_WAIT_TIME_PER_TASK))
            print("TODO")
            self.close()
            exit(0)

    def _request(self, fun, *args, **kwargs):
        """ Wrapper method so we don't have to write the kwargs on every api call"""
        kwargs["headers"] = {
            'User-Agent': self.user_agent,
        }
        return fun(*args, **kwargs)

    def get_status(self, status_id) -> Tweet:
        return self._request(self._api.get_status, status_id)

    def get_timeline(self) -> List[Tweet]:
        return self._request(self._api.home_timeline)

    def follow(self, user_id) -> User:
        return self._request(self._api.create_friendship, user_id)

    def close(self):
        self._closed = True

    @property
    def proxy(self):
        return self._proxy

    @property
    def user_agent(self) -> str:
        return self._user_agent

    @property
    def raw_api(self) -> TweepyWrapper:
        return self._api
