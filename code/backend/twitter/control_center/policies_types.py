from enum import IntEnum


class PoliciesTypes(IntEnum):
    REQUEST_TWEET_LIKE = 1
    REQUEST_TWEET_RETWEET = 2
    REQUEST_TWEET_REPLY = 3
    REQUEST_FOLLOW_USER = 4
    FIRST_TIME = 5

    def __str__(self):
        return self.name
