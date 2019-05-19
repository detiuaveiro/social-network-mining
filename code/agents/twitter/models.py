from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Dict, Any, Optional, List

import tweepy

from utils import snowflake_time

__all__ = ["Colour", "Color", "BaseModel", "User", "Tweet"]


class Colour:
    """Represents a generic Twitter colour.
      There is an alias for this called Color.
      .. container:: operations
          .. describe:: x == y
               Checks if two colours are equal.
          .. describe:: x != y
               Checks if two colours are not equal.
          .. describe:: hash(x)
               Return the colour's hash.
          .. describe:: str(x)
               Returns the hex format for the colour.
      Attributes
      ------------
      value: :class:`int`
          The raw integer colour value.
      """

    __slots__ = ("value",)

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Expected int!")
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Colour) and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '#{:0>6x}'.format(self.value)

    def __repr__(self):
        return '<Colour value=%s>' % self.value

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def from_hex(cls, value: str) -> Colour:
        """Factory method for a :class:`Colour`  from an Hex Value."""
        return cls(int(value, 16))

    @classmethod
    def from_rgb(cls, r, g, b) -> Colour:
        """Factory method for a :class:`Colour` from an RGB tuple."""
        return cls((r << 16) + (g << 8) + b)

    def to_json(self):
        return str(self)


Color = Colour


@dataclass
class BaseModel(abc.ABC):
    """
    Common attributes for the object models for Twitter's models
    Attributes
    -----------
    id: :class:`int`
        The model's unique ID.
    id_str: :class:`str`
        The `str` representation of the model's unique ID
    """
    _api: tweepy.API
    _json: Dict[Any]

    @property
    @abc.abstractmethod
    def created_at(self):
        """Returns the model's creation time in UTC."""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def from_json(api, json):
        """Returns an instance of this Model from the JSON supplied"""
        raise NotImplementedError

    @abc.abstractmethod
    def to_json(self):
        raise NotImplementedError


@dataclass
class User(BaseModel):
    """

    """
    id: int
    name: str
    screen_name: str
    location: str
    description: str
    url: str
    protected: bool
    followers_count: int
    friends_count: int
    listed_count: int

    @property
    def created_at(self):
        """Returns the model's creation time in UTC."""
        return str(snowflake_time(self.id))

    following: bool
    follow_request_sent: bool
    favourites_count: int
    verified: bool
    statuses_count: int
    lang: str
    contributors_enabled: bool
    profile_background_tile: bool
    profile_background_color: Colour
    profile_background_image_url: str
    profile_background_image_url_https: str
    profile_image_url: str
    profile_image_url_https: str
    profile_link_color: Colour
    profile_sidebar_border_color: Colour
    profile_sidebar_fill_color: Colour
    profile_text_color: Colour
    profile_use_background_image: bool
    has_extended_profile: bool
    default_profile: bool
    default_profile_image: bool
    notifications: bool
    suspended: bool = False

    def to_json(self):
        """
        Returns the JSON that represents this entity
        """
        return self._json

    @staticmethod
    def from_json(api, json: dict):
        """Returns an instance of this Model from the JSON supplied"""
        # copying the
        unclean_json = json
        # removing unused attributes
        ignore_attributes = ["id_str", "entities", "created_at", "utc_offset", "time_zone",
                             "geo_enabled", "is_translator", "is_translation_enabled",
                             "needs_phone_verification", "translator_type", "status",
                             "profile_banner_url", "profile_location"]
        for i in ignore_attributes:
            unclean_json.pop(i, None)
        # To make things easier for to us, we're going transforming some of the attributes into objects
        # TODO: Currently only for colours, do the same for entities
        unclean_json["profile_background_color"] = Colour.from_hex(
            unclean_json["profile_background_color"])
        unclean_json["profile_link_color"] = Colour.from_hex(unclean_json["profile_link_color"])
        unclean_json["profile_sidebar_border_color"] = Colour.from_hex(
            unclean_json["profile_sidebar_border_color"])
        unclean_json["profile_sidebar_fill_color"] = Colour.from_hex(
            unclean_json["profile_sidebar_fill_color"])
        unclean_json["profile_text_color"] = Colour.from_hex(unclean_json["profile_text_color"])
        # Then make use of kwargs to do the init properly
        # but not before storing the old json and passing the API instance
        # so we can write the following semantically
        return User(_api=api, _json=unclean_json, **unclean_json)

    def timeline(self, **kwargs) -> List[Tweet]:
        """
        Gets the user's timeline.
        Parameters
        ----------
        kwargs : Dict[Any]
            Optional arguments

        Returns
        -------
        tweets: List[Tweet]
            List of Tweet objects from the User's Timeline
        """
        return self._api.user_timeline(user_id=self.id, **kwargs)

    def friends(self, **kwargs) -> List[User]:
        """
        Gets the user's friends.
        Parameters
        ----------
        kwargs : Dict[Any]
            Optional arguments

        Returns
        -------
        friends: List[User]
            List of User objects that are friends of the user
        """
        return self._api.friends(user_id=self.id, **kwargs)

    def followers(self, **kwargs) -> List[User]:
        """
        Gets the user's followers.
        Parameters
        ----------
        kwargs : Dict[Any]
            Optional arguments

        Returns
        -------
        friends: List[User]
            List of User objects that are friends of the user
        """
        return self._api.followers(user_id=self.id, **kwargs)

    def follow(self):
        if self.following:
            return
        self._api.create_friendship(user_id=self.id)
        self.following = True
        self._json["following"] = True

    def unfollow(self):
        if not self.following:
            return
        self._api.destroy_friendship(user_id=self.id)
        self.following = False
        self._json["following"] = False


@dataclass
class Tweet(BaseModel):
    id: int
    text: str

    @property
    def created_at(self):
        """Returns the model's creation time in UTC."""
        return str(snowflake_time(self.id))

    truncated: str
    entities: Dict
    source: str
    in_reply_to_status_id: Optional[int]
    in_reply_to_user_id: Optional[int]
    in_reply_to_screen_name: Optional[str]
    user: User
    is_quote_status: bool
    retweet_count: int
    favorite_count: int
    favorited: bool
    retweeted: bool
    possibly_sensitive: bool
    lang: str

    def to_json(self):
        unclean = self._json
        # we don't need to send these 2 attribute
        unclean.pop("favorited", None)
        unclean.pop("retweeted", None)
        # and also cleaning up the tweet object, by not filling in with the user
        unclean["user"] = unclean["user"].id
        return unclean

    @staticmethod
    def from_json(api, json: dict):
        """Returns an instance of this Model from the JSON supplied"""
        # copying the
        unclean_json = json
        # removing unused attributes
        ignore_attributes = ["id_str", "created_at", "in_reply_to_status_id_str",
                             "in_reply_to_user_id_str", "geo", "coordinates", "place",
                             "contributors"]
        for i in ignore_attributes:
            unclean_json.pop(i, None)
        # Filling in with User object for handiness
        unclean_json["user"] = User.from_json(api, unclean_json["user"])
        return Tweet(_api=api, _json=unclean_json, **unclean_json)

    def retweet(self):
        if self.retweeted:
            return
        self._api.retweet(self.id)
        self.retweeted = True

    def like(self):
        # Unnecessary to make the API call in this case
        if self.favorited:
            return
        self._api.create_favorite(self.id)
        self.favorited = True

    def dislike(self):
        # Unnecessary to make the API call in this case
        if not self.favorited:
            return
        self._api.destroy_favorite(self.id)
        self.favorited = False
