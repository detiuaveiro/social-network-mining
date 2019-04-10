# in seconds
MIN_WAIT_TIME_PER_TASK = 60
# in seconds
MAX_WAIT_TIME_PER_TASK = MIN_WAIT_TIME_PER_TASK * 10
# Default User Agent
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
# Word per minute to "read"
WPM = 253
# for keyword-related filters. Should not be 0, to avoid considering spam
MIN_KEYWORD_THRESHOLD = 0.0
# Other-user related
MIN_USER_TIMELINE_TWEETS = 5
MAX_USER_TIMELINE_TWEETS = 10
# Our Timeline
MIN_HOME_TIMELINE_TWEETS = 20
MAX_HOME_TIMELINE_TWEETS = 40

# Not recommended below 15 mins
MIN_RUN_TIME = 15 * 60
# Not recommended below 30 mins
MAX_RUN_TIME = 60 * 60

FIND_NEW_SUGGESTIONS_CHANCE = 2

# Should be high enough to avoid getting spotted
RETWEET_CHANCE = 0.9

# Can be reasonably low
FAVOURITE_CHANCE = 0.5

# Max retries before exiting from task-routine
MAX_RETRIES = 5

# Messagin-related settings
TASKS_EXCHANGE = "tasks_deliver"
LOG_EXCHANGE = "bot_logs"
TASKS_QUEUE_PREFIX = "bot"
TASKS_ROUTING_KEY_PREFIX = "tasks.twitter"
QUERY_EXCHANGE = "queries"
DATA_EXCHANGE = "twitter_data"
