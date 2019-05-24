from enum import IntEnum


class Task(IntEnum):
    """
    Enum for the tasks the bot is able to run. Received by the bot from the server.
    """
    FOLLOW_USERS = 1
    FIND_BY_KEYWORDS = 2
    LIKE_TWEETS = 3
    RETWEET_TWEETS = 4
    REPLY_TWEETS = 5
    FIND_FOLLOWERS = 6

    def __str__(self):
        return self.name


class MessageType(IntEnum):
    """
    Enum for the Messages sent by the bot to the server.
    """
    EVENT_USER_FOLLOWED = 1
    EVENT_TWEET_LIKED = 2
    EVENT_TWEET_RETWEETED = 3
    EVENT_TWEET_REPLIED = 4
    QUERY_TWEET_LIKE = 5
    QUERY_TWEET_RETWEET = 6
    QUERY_TWEET_REPLY = 7
    QUERY_FOLLOW_USER = 8
    SAVE_USER = 9
    SAVE_TWEET = 10
    EVENT_USER_BLOCKED = 11

    def __str__(self):
        return self.name
