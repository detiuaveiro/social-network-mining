from typing import List

import tweepy
from models import User, Tweet


class TweepyWrapper(tweepy.API):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def get_status(self, status_id) -> Tweet:
        """

        Parameters
        ----------
        status_id : :class:`int`

        Returns
        -------

        """
        unclean_status = super().get_status(status_id)
        return unclean_status

    def home_timeline(self) -> List[Tweet]:
        unclean_statuses = super().home_timeline()
        return unclean_statuses

    def create_friendship(self, user_id) -> User:
        unclean_user = super().create_friendship(user_id)
        return unclean_user
