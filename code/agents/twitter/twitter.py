from typing import List

import tweepy

from interfaces import Bot
from interfaces import Storage
from storage import Neo4JWrapper


class TwitterBot(Bot):
    def __init__(self, **options):
        self._closed = False
        self._user_agent = options.pop("user_agent")
        self._proxy = options.pop("tor_proxy", None)
        self._storage: Storage = None
        self._api: tweepy.API = None

    def connect_to_storage(self, **kwargs):
        self._storage = Neo4JWrapper(**kwargs)

    def connect_to_api(self, **kwargs):
        auth = tweepy.OAuthHandler(kwargs.pop("consumer_key"), kwargs.pop("consumer_secret"))
        auth.set_access_token(kwargs.pop("access_token"), kwargs.pop("access_token_secret"))
        self._api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                               proxy=self._proxy)

    def start(self, **kwargs):
        db_settings = kwargs.pop("database")
        self.connect_to_storage(**db_settings)
        api_settings = kwargs.pop("api")
        self.connect_to_api(**api_settings)

    def run(self):
        while not self._closed:
            for i in self.get_timeline():
                print(i)
            self.close()

    def _request(self, fun, *args, **kwargs):
        """ Wrapper method so we don't have to write the kwargs on every api call"""
        kwargs["headers"] = {
                'User-Agent': self.user_agent,
        }
        return fun(*args, **kwargs)

    def get_status(self, status_id) -> List[tweepy.Status]:
        return self._request(self._api.get_status, status_id)

    def get_timeline(self) -> List[tweepy.Status]:
        return self._request(self._api.home_timeline)

    def follow(self, user_id) -> tweepy.User:
        return self._request(self._api.create_friendship, user_id)

    def close(self):
        self._closed = True
        self._storage.close()

    @property
    def proxy(self):
        return self._proxy

    @property
    def storage(self) -> Storage:
        return self._storage

    @property
    def user_agent(self) -> str:
        return self._user_agent

    @property
    def raw_api(self) -> tweepy.API:
        return self._api
