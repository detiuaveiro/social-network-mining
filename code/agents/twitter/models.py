import typing
import abc

from utils import snowflake_time


class BaseModel(abc):
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
    in_reply_to_status_id: Optional[:class:`int`]
         If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s ID.
    in_reply_to_user_id: Optional[:class:`int`]
        If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s author ID. This will not necessarily always be the user directly mentioned in the Tweet.
    in_reply_to_screen_name: Optional[:class:`str`]
        If the represented Tweet is a reply, this field will contain the screen name of the original Tweet’s author.
    user: :class:`User`
        The user who posted this Tweet.
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
    """
    __slots__ = ("_json", "_created_at", "id", "text", "user", "entities")

    def __init__(self, *, data):
        self._created_at = data["created_at"]  # for debug purposes
        self.id: int = int(data["id"])
        self.text: str = data["text"]
        self.source: str = data["source"]
        self.truncated: bool = data.get("truncated", False)

    @property
    def created_at(self) -> str:
        """Returns the Tweets's creation time in UTC."""
        return str(snowflake_time(self.id))
