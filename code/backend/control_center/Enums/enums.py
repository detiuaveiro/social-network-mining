from enum import IntEnum

class MessageTypes(IntEnum):
    USER_FOLLOWED = 1
    TWEET_LIKED = 2
    TWEET_RETWEETDED = 3
    TWEET_REPLIED = 4
    REQUEST_TWEET_LIKE = 5
    REQUEST_TWEET_RETWEET = 6
    REQUEST_TWEET_REPLY = 7
    REQUEST_FOLLOW_USER = 8
    SAVE_USER = 9
    SAVE_TWEET = 10
    ERROR_BOT = 11
    FIND_FOLLOWERS = 12
    SAVE_DIRECT_MESSAGES = 13

class ResponseTypes(IntEnum):
    FOLLOW_USERS = 1
    FIND_BY_KEYWORDS = 2
    LIKE_TWEETS = 3
    RETWEET_TWEETS = 4
    POST_TWEETS = 5
    FIND_FOLLOWERS = 6

class Neo4jTypes(IntEnum):
    CREATE_BOT = 1
    CREATE_USER = 2
    CREATE_RELATION_BOT_USER = 3
    SEARCH_USER = 4
    UPDATE_USER = 5
    SEARCH_BOT = 6
    UPDATE_BOT = 7
    CREATE_RELATION_USER_USER = 8
    CREATE_RELATION_BOT_BOT = 9

class PoliciesTypes(IntEnum):
    REQUEST_TWEET_LIKE = 1
    REQUEST_TWEET_RETWEET = 2
    REQUEST_TWEET_REPLY = 3
    REQUEST_FOLLOW_USER = 4
    FIRST_TIME = 5