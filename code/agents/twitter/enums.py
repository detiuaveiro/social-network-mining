from enum import IntEnum


class Task(IntEnum):
    FOLLOW_USERS = 1
    FIND_BY_KEYWORDS = 2
    LIKE_TWEETS = 3
    RETWEET_TWEETS = 4

    def __str__(self):
        return self.name


class MessageType(IntEnum):
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

    def __str__(self):
        return self.name
