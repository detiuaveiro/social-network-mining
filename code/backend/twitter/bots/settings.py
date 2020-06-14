import os


# -----------------------------------------------------------
# Tweepy errors
# -----------------------------------------------------------

ACCOUNT_SUSPENDED_ERROR_CODES = [63, 64, 326]
FOLLOW_USER_ERROR_CODE = 161


# -----------------------------------------------------------
# Tweepy settings
# -----------------------------------------------------------

MAX_NUMBER_TWEETS_RETRIEVE_TIMELINE = 5


# -----------------------------------------------------------
# Redis
# -----------------------------------------------------------

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')


# -----------------------------------------------------------
# Other settings
# -----------------------------------------------------------

BULK_MESSAGES_SIZE_LIMIT_SEND = 20

WAIT_TIME_BETWEEN_WORK = 60*60*3            # three hours
WAIT_TIME_RANDOM_STOP = 60*60               # an hour
WAIT_TIME_NO_MESSAGES = 60*15               # 15 minutes
BOT_TTL = 60*60*24							# one day
