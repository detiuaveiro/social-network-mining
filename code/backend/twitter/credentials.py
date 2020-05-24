import os

# -----------------------------------------------------------
#  MONGO 
# -----------------------------------------------------------
MONGO_URL = os.environ.get('MONGO_URL', 'localhost')
MONGO_PORT = 27017
MONGO_DB = os.environ.get('MONGO_DB', 'twitter')
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'admin')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'admin')
MONGO_FULL_URL = f"{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_URL}:{MONGO_PORT}/{MONGO_DB}"


# -----------------------------------------------------------
# POSTGRES 
# -----------------------------------------------------------
POSTGRES_URL = os.environ.get('POSTGRES_URL', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
POSTGRES_FULL_URL = f"{POSTGRES_URL}:{POSTGRES_PORT}"
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'twitter')
POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME', 'admin')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'admin')


# -----------------------------------------------------------
# REDIS FOR THE REST API
# -----------------------------------------------------------
REDIS_URL = os.environ.get('REDIS_URL', '172.26.0.2')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_FULL_URL = f"redis://{REDIS_URL}:{REDIS_PORT}/1"
REDIS_KEY_PREFIX = os.environ.get('REDIS_KEY_PREFIX', 'pi_rest')


# ----------------------------------------------------------- 
# RABBITMQ
# -----------------------------------------------------------
RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'localhost')
RABBITMQ_PORT = 5672
RABBITMQ_HTTP_PORT = 15672
RABBITMQ_FULL_URL = f"{RABBITMQ_URL}:{RABBITMQ_PORT}"
RABBITMQ_FULL_HTTP_URL = f"{RABBITMQ_URL}:{RABBITMQ_HTTP_PORT}"
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME', 'admin')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'admin')

# Queues and Exchanges
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

TWEET_EXCHANGE = "tweet_data"
TWEET_ROUTING_KEY = "data.tweet"

USER_EXCHANGE = "user_data"
USER_ROUTING_KEY = "data.user"

TWEET_LIKE_EXCHANGE = "tweet_like_data"
TWEET_LIKE_ROUTING_KEY = "data.tweet_like"

QUERY_FOLLOW_USER_EXCHANGE = "query_follow_user_data"
QUERY_FOLLOW_USER_ROUTING_KEY = "data.query_follow_user"

QUERY_TWEET_LIKE_EXCHANGE = "query_like_data"
QUERY_TWEET_LIKE_ROUTING_KEY = "data.query_follow_user"

QUERY_TWEET_RETWEET_EXCHANGE = "query_retweet_data"
QUERY_TWEET_RETWEET_ROUTING_KEY = "data.query_follow_user"

QUERY_TWEET_REPLY_EXCHANGE = "query_reply_data"
QUERY_TWEET_REPLY_ROUTING_KEY = "data.query_follow_user"

QUERY_KEYWORDS_EXCHANGE = "query_keywords_data"
QUERY_KEYWORDS_ROUTING_KEY = "data.query_follow_user"

TASK_FOLLOW_EXCHANGE = "follow_deliver"
TASK_FOLLOW_ROUTING_KEY_PREFIX = "follow.twitter"
TASK_FOLLOW_QUEUE = "follow"

SERVICE_QUERY_EXCHANGE = "follow_queries"
SERVICE_QUERY_ROUTING_KEY = "follow_queries.twitter"

API_QUEUE = 'API'
API_FOLLOW_QUEUE = 'API_FOLLOW'


# -----------------------------------------------------------
# NEO4J
# -----------------------------------------------------------
NEO4J_URL = os.environ.get('NEO4J_URL', 'localhost')
NEO4J_PORT = 7687
NEO4J_FULL_URL = f"{NEO4J_URL}:{NEO4J_PORT}"
NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'neo4jPI')


# -----------------------------------------------------------
# ParlAI
# -----------------------------------------------------------
PARLAI_URL = os.environ.get('PARLAI_URL', 'localhost')
PARLAI_PORT = 5555
