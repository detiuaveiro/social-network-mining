from enum import IntEnum


class Task(IntEnum):
    FOLLOW_USERS = 1
    FIND_BY_KEYWORDS = 2

    def __str__(self):
        return self.name


class MessageType(IntEnum):
    USER_FOLLOWED = 1
    TWEET_LIKED = 2
    TWEET_RETWEED = 3
    ASK_FOLLOW_USER = 4
    SEND_USER = 5
    SEND_TWEET = 6

    def __str__(self):
        return self.name
