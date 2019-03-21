from __future__ import annotations
from typing import Optional, Dict, List
import abc
from utils import snowflake_time


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


Color = Colour


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
    __slots__ = ()

    @property
    @abc.abstractmethod
    def created_at(self):
        """Returns the model's creation time in UTC."""
        raise NotImplementedError


class Tweet(BaseModel):
    """The class that represents the `Tweet` object from the Twitter API
    Attributes
    -----------
    created_at: :class:`str`
        UTC time when this Tweet was created.
    id: :class:`int`
        The integer representation of the unique identifier for this Tweet.
    text: :class:`str`
        The actual UTF-8 text of the status update.
    source: :class:`str`
        Utility used to post the Tweet, as an HTML-formatted string.
        Tweets from the Twitter website have a source value of web
    truncated: :class:`bool`
        Indicates whether the value of the text parameter was truncated, for example, as a result of a retweet exceeding the original Tweet text length limit of 140 characters.
        Truncated text will end in ellipsis, like this `...`
        Since Twitter now rejects long Tweets vs truncating them, the large majority of Tweets will have this set to false.
        Note that while native retweets may have their toplevel text property shortened, the original text will be available under the retweeted_status object and the truncated parameter will be set to the value of the original status (in most cases, false ).
    user: :class:`User`
        The user who posted this Tweet.
    in_reply_to_status_id: Optional[:class:`int`]
         If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s ID.
    in_reply_to_user_id: Optional[:class:`int`]
        If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s author ID. This will not necessarily always be the user directly mentioned in the Tweet.
    in_reply_to_screen_name: Optional[:class:`str`]
        If the represented Tweet is a reply, this field will contain the screen name of the original Tweet’s author.
    coordinates: Optional[:class:`Coordinates`]
        Represents the geographic location of this Tweet as reported by the user or client application.
    place: Optional[:class:`Place`]
        When present, indicates that the tweet is associated (but not necessarily originating from) a Place.
    quoted_status_id: Optional[:class:`int`]
        This field only surfaces when the Tweet is a quote Tweet. This field contains the integer value Tweet ID of the quoted Tweet
    is_quote_status: :class:`bool`
        Indicates whether this is a Quoted Tweet.
    quoted_status: Optional[:class:`Tweet`]
        This field only surfaces when the Tweet is a quote Tweet. This attribute contains the Tweet object of the original Tweet that was quoted.
    retweed_status: Optional[:class:`Tweet`]
        Users can amplify the broadcast of Tweets authored by other users by retweeting . Retweets can be distinguished from typical Tweets by the existence of a retweeted_status attribute. This attribute contains a representation of the original Tweet that was retweeted. Note that retweets of retweets do not show representations of the intermediary retweet, but only the original Tweet. (Users can also unretweet a retweet they created by deleting their retweet.)
    quote_count: Optional[:class:`int`]
        Indicates approximately how many times this Tweet has been quoted by Twitter users. (Premium/Enterprise Only)
    reply_count: :class:`int`
        Number of times this Tweet has been replied to. (Premium/Enterprise Only)
    retweet_count: :class:`int`
        Number of times this Tweet has been retweeted.
    favorite_count: :class:`int`
        Indicates approximately how many times this Tweet has been liked by Twitter users.
    entities: :class:`Entities`
        Entities which have been parsed out of the text of the Tweet.
    extended_entities: :class:`Extended Entities`
        When between one and four native photos or one video or one animated GIF are in Tweet, contains an array 'media' metadata.
    favorited: :class:`bool`
        Indicates whether this Tweet has been liked by the authenticating user. Example
    retweeted: :class:`bool`
        Indicates whether this Tweet has been retweeted by the authenticating user. Example
    possibly_sensitive: Optional[:class:`bool`]
        This field only surfaces when a Tweet contains a link.
    filter_level: :class:`str`
        Indicates the maximum value of the filter_level parameter which may be used and still stream this Tweet. So a value of medium will be streamed on none, low, and medium streams.
    """
    __slots__ = (
        "_json",
        "_created_at",
        "id",
        "text",
        "source",
        "truncated",
        "in_reply_to_status_id",
        "in_reply_to_user_id",
        "in_reply_to_screen_name",
        "user",
        "coordinates",
        "place",
        "quoted_status_id",
        "is_quote_status",
        "quoted_status",
        "retweeted_status",
        "quote_count",
        "reply_count",
        "retweet_count",
        "favourite_count",
        "entities",
        "extended_entities",
        "favorited",
        "retweeted",
        "possibly_sensitive",
        "filter_level",
    )

    def __init__(self, *, data):
        self._json = data["_json"]
        self._created_at = data["created_at"]  # for debug purposes
        self.id: int = int(data["id"])
        self.text: str = data["text"]
        self.source: str = data["source"]
        self.truncated: bool = bool(data.get("truncated", False))
        # Optional
        if data.get("in_reply_to_status_id", None) is not None:
            self.in_reply_to_status_id: Optional[int] = int(data["in_reply_to_status_id"])
        else:
            self.in_reply_to_status_id: Optional[int] = None
        # optional
        if data.get("in_reply_to_user_id", None) is not None:
            self.in_reply_to_user_id: Optional[int] = int(data["in_reply_to_user_id"])
        else:
            self.in_reply_to_user_id: Optional[int] = None
        # optional
        self.in_reply_to_screen_name: str = data.get("in_reply_to_screen_name", "")
        self.user: User = User.from_data(data["user"])
        # TODO: make proper Coordinates class
        self.coordinates: Dict = data.get("coordinates", None)
        # TODO: make proper Place class
        self.place: Dict = data.get("place", None)
        # optional
        if data.get("quoted_status_id", None) is not None:
            self.quoted_status_id: Optional[int] = int(data["quoted_status_id"])
        else:
            self.quoted_status_id: Optional[int] = None

        self.is_quote_status: bool = bool(data["is_quote_status"])
        self.quoted_status: Tweet = data.get("quoted_status", None)
        self.retweeted_status: Tweet = data.get("retweeted_status", None)
        # get because it's only available to premium
        if data.get("quote_count", None) is not None:
            self.quote_count: Optional[int] = int(data["quote_count"])
        else:
            self.quote_count: Optional[int] = None

        # get because it's only available to premium
        if data.get("reply_count", None) is not None:
            self.reply_count: Optional[int] = int(data["reply_count"])
        else:
            self.reply_count: Optional[int] = None

        self.retweet_count: int = int(data["retweet_count"])
        self.favourite_count: int = int(data["favourite_count"])
        # TODO: Make proper Entities class
        self.entities: Dict = (data["entities"])
        # TODO: make proper Extended Entities class
        self.extended_entities: Dict = data["extended_entities"]
        self.favorited: bool = bool(data.get("favorited", False))
        self.retweeted: bool = bool(data.get("retweeted", False))
        self.possibly_sensitive: bool = bool(data.get("possibly_sensitive", False))
        self.filter_level: str = data["filter_level"]

    @property
    def created_at(self) -> str:
        """Returns the Tweets's creation time in UTC."""
        return str(snowflake_time(self.id))


class User(BaseModel):
    __slots__ = (
        "_created_at",
        "id",
        "name",
        "screen_name",
        "location",
        "url",
        "description",
        "derived",
        "protected",
        "verified",
        "followers_count",
        "friends_count",
        "listed_count",
        "favourites_count",
        "statuses_count",
        "geo_enabled",
        "contributors_enabled",
        "profile_background_color",
        "profile_background_image_url",
        "profile_background_image_url_https",
        "profile_background_tile",
        "profile_banner_url",
        "profile_image_url",
        "profile_image_url_https",
        "profile_link_color",
        "profile_sidebar_border_color",
        "profile_sidebar_fill_color",
        "profile_text_color",
        "profile_use_background_image",
        "default_profile",
        "default_profile_image",
        "withheld_in_countries",
        "withheld_scope"
    )

    def __init__(self, *, data):
        self._json = data["_json"]
        self._created_at: str = data["created_at"]  # for debug purposes
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.screen_name: str = data["screen_name"]
        self.location: str = data.get("location", "")
        self.url: str = data.get("url", "")
        self.description: str = data.get("description", "")
        self.derived: Dict[List[Dict]] = data["derived"]
        self.protected: bool = data["protected"]
        self.verified: bool = data["verified"]
        self.followers_count: int = int(data["followers_count"])
        self.friends_count: int = int(data["friends_count"])
        self.listed_count: int = int(data["listed_count"])
        self.favourites_count: int = int(data["favourites_count"])
        self.statuses_count: int = int(data["statuses_count"])
        self.geo_enabled: bool = bool(data["geo_enabled"])
        self.contributors_enabled: bool = bool(data["contributors_enabled"])
        self.profile_background_color: Colour = Colour.from_hex(data["profile_background_color"])
        self.profile_background_image_url: str = data["profile_background_image_url"]
        self.profile_background_image_url_https: str = data["profile_background_image_url_https"]
        self.profile_background_tile: bool = bool(data["profile_background_tile"])
        self.profile_banner_url: str = data["profile_banner_url"]
        self.profile_image_url: str = data["profile_image_url"]
        self.profile_image_url_https: str = data["profile_image_url_https"]
        self.profile_link_color: Colour = Colour.from_hex(data["profile_link_color"])
        self.profile_sidebar_border_color: Colour = Colour.from_hex(
            data["profile_sidebar_border_color"])
        self.profile_sidebar_fill_color: Colour = Colour.from_hex(
            data["profile_sidebar_fill_color"])
        self.profile_text_color: Colour = Colour.from_hex(data["profile_text_color"])
        self.profile_use_background_image: bool = bool(data["profile_use_background_image"])
        self.default_profile: bool = bool(data["default_profile"])
        self.default_profile_image: bool = bool(data["default_profile_image"])
        self.withheld_in_countries: List[str] = data["withheld_in_countries"]
        self.withheld_scope: str = data["withheld_scope"]

    @property
    def created_at(self) -> str:
        """Returns the Tweets's creation time in UTC."""
        return str(snowflake_time(self.id))

    @staticmethod
    def from_data(user_data) -> User:
        return User(data=user_data)
