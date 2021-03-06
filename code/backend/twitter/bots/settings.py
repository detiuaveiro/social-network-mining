import os


# -----------------------------------------------------------
# Tweepy errors
# -----------------------------------------------------------

ACCOUNT_SUSPENDED_ERROR_CODES = [63, 64, 326]
FOLLOW_USER_ERROR_CODE = 161


# -----------------------------------------------------------
# Tweepy settings
# -----------------------------------------------------------

MAX_NUMBER_TWEETS_RETRIEVE_TIMELINE = 3


# -----------------------------------------------------------
# Redis
# -----------------------------------------------------------

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')


# -----------------------------------------------------------
# Other settings
# -----------------------------------------------------------

BULK_MESSAGES_SIZE_LIMIT_SEND = 8

WAIT_TIME_BETWEEN_WORK = 60*60*3            # three hours
WAIT_TIME_RANDOM_STOP = 60*60*0.5           # half an hour
WAIT_TIME_NO_MESSAGES = 60*30               # half an hour
BOT_TTL = 60*60*24							# a day
WAIT_TIME_NEW_SETUP = 60*60*24              # a day
