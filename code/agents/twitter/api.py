import logging
from typing import Callable, Optional, Any, List

import tweepy
from tweepy.binder import bind_api
from tweepy.parsers import ModelParser
import utils

from models import User, Tweet, DirectMessage

log = logging.getLogger("bot-agents")
log.setLevel(logging.DEBUG)

class DirectMessagesParserWrapper(ModelParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def parse(self, method, payload):
        if not method.payload_type == 'direct_message':
            return super().parse(method, payload)
        events = utils.from_json(payload)
        return [DirectMessage.from_json(method.api, i) for i in events['events']]


class TweepyWrapper(tweepy.API):
    def __init__(self, *,
                 consumer_key: str,
                 consumer_secret: str,
                 token: str,
                 token_secret: str,
                 user_agent: str,
                 tor_proxies: str = ""):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(token, token_secret)
        super().__init__(auth_handler=auth, wait_on_rate_limit=True, proxy=tor_proxies)
        # Getting the reference to the super class to make it more explicit
        # we're calling the tweepy's methods
        # And also become Tweepy doesn't provide an interface of its methods,
        # so we're forced to extend the class to be able to provide the same functionality
        self._tweepy: tweepy.API = super()
        self.user_agent = user_agent

        # we're replacing Tweepy's parser because of it not being updated for direct messages
        self.parser = DirectMessagesParserWrapper()

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
        # Since we're making our own version of the models,
        # we're going to ignore everything except the json
        try:
            dirty_data = fun(*args, **kwargs)
        # we need to do this type error because for some reason, tweepy.lookup_users doesn't accept the header kwargs....
        except TypeError as e:
            log.warning(f"Type error found in {fun.__name__}, removing headers! {e}")
            kwargs.pop("headers", None)
            dirty_data = fun(*args, **kwargs)
        # Wrapper for User
        data_type = type(dirty_data)
        if data_type == tweepy.models.User:
            return User.from_json(self, dirty_data._json)
        elif data_type == tweepy.models.Status:
            return Tweet.from_json(self, dirty_data._json)
        # List of something
        elif data_type == list or data_type == tweepy.models.ResultSet:
            # if there's any elements
            if dirty_data:
                # check the type of the first
                first_type = type(dirty_data[0])
                if first_type == tweepy.models.User:
                    return [User.from_json(self, u._json) for u in dirty_data]
                elif first_type == tweepy.models.Status:
                    return [Tweet.from_json(self, u._json) for u in dirty_data]
        # edge case, return data
        return dirty_data

    def user_timeline(self, **kwargs) -> List[Tweet]:
        __doc__ = self._tweepy.user_timeline.__doc__
        user_id = kwargs.pop("user_id")
        return self._request(self._tweepy.user_timeline, user_id=user_id, **kwargs)

    def followers(self, **kwargs):
        __doc__ = self._tweepy.followers.__doc__
        user_id = kwargs.pop("user_id")
        return self._request(self._tweepy.followers, user_id=user_id, **kwargs)

    def create_friendship(self, **kwargs):
        __doc__ = self._tweepy.create_friendship.__doc__
        user_id = kwargs.pop("user_id")
        self._request(self._tweepy.create_friendship, user_id=user_id, **kwargs)

    def destroy_friendship(self, **kwargs):
        __doc__ = self._tweepy.destroy_friendship.__doc__
        user_id = kwargs.pop("user_id")
        self._request(self._tweepy.destroy_friendship, user_id=user_id, **kwargs)

    def retweet(self, **kwargs):
        __doc__ = self._tweepy.retweet.__doc__
        tweet_id = kwargs.pop("tweet_id")
        self._request(self._tweepy.retweet, tweet_id=tweet_id, **kwargs)

    def create_favourite(self, **kwargs):
        __doc__ = self._tweepy.create_favorite.__doc__
        tweet_id = kwargs.pop("tweet_id")
        self._request(self._tweepy.create_favorite, tweet_id=tweet_id, **kwargs)

    def destroy_favorite(self, **kwargs):
        __doc__ = self._tweepy.destroy_favorite.__doc__
        tweet_id = kwargs.pop("tweet_id")
        self._request(self._tweepy.destroy_friendship, tweet_id=tweet_id, **kwargs)

    def verify_credentials(self) -> User:
        __doc__ = self._tweepy.verify_credentials.__doc__
        return self._request(self._tweepy.verify_credentials)

    def get_status(self, **kwargs) -> Tweet:
        __doc__ = self._tweepy.get_status.__doc__
        tweet_id = kwargs.pop("tweet_id")
        return self._request(self._tweepy.get_status, id=tweet_id)

    def get_user(self, **kwargs) -> User:
        __doc__ = self._tweepy.get_status.__doc__
        return self._request(self._tweepy.get_user, **kwargs)

    def home_timeline(self, **kwargs) -> List[Tweet]:
        __doc__ = self._tweepy.home_timeline.__doc__
        return self._request(self._tweepy.home_timeline, **kwargs)

    def lookup_users(self, *, user_ids: List[int], **kwargs) -> List[User]:
        __doc__ = self._tweepy.lookup_users.__doc__
        return self._request(self._tweepy.lookup_users, user_ids=user_ids, **kwargs)

    def user_timeline(self, **kwargs) -> List[Tweet]:
        __doc__ = self._tweepy.user_timeline.__doc__
        user_id = kwargs.pop("user_id")
        return self._request(self._tweepy.user_timeline, user_id=user_id, **kwargs)

    def direct_messages(self, **kwargs) -> List[DirectMessage]:
        __doc__ = self._tweepy.direct_messages.__doc__

        api_call = bind_api(api=self, path='/direct_messages/events/list.json',
                        payload_type='direct_message', payload_list=True,
                        allowed_param=['count', 'cursor'], require_auth=True)
        return self._request(api_call, **kwargs)

    def update_status(self, **kwargs) -> Tweet:
        __doc__ = self._tweepy.update_status.__doc__
        return self._request(self._tweepy.update_status, **kwargs)