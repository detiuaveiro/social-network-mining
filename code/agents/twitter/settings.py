# -----------------------------------------------------------
# messaging queuing
# -----------------------------------------------------------

VHOST = "PI"

TASKS_EXCHANGE = "tasks_deliver"
TASKS_ROUTING_KEY_PREFIX = "tasks.twitter"
TASKS_QUEUE_PREFIX = "bot"

LOG_EXCHANGE = "logs"
LOG_ROUTING_KEY = "logs.twitter"

QUERY_EXCHANGE = "queries"
QUERY_ROUTING_KEY = "queries.twitter"

DATA_EXCHANGE = "twitter_data"
DATA_ROUTING_KEY = "data.twitter"


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
# RabbitQM credentials
# -----------------------------------------------------------

# RABBIT_USERNAME = 'pi_rabbit_admin'
# RABBIT_PASSWORD = 'yPvawEVxks7MLg3lfr3g'

RABBIT_USERNAME = 'admin'
RABBIT_PASSWORD = 'admin'
