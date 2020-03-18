import os

# -----------------------------------------------------------
#  MONGO 
# -----------------------------------------------------------
MONGO_URL = os.environ.get('MONGO_URL', 'localhost')
MONGO_PORT = 27017
MONGO_FULL_URL = f"{MONGO_URL}:{MONGO_PORT}"
MONGO_DB = os.environ.get('MONGO_DB', 'twitter')
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'admin')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'admin')

# -----------------------------------------------------------
# POSTGRES 
# -----------------------------------------------------------
POSTGRES_URL = os.environ.get('POSTGRES_URL', 'localhsot')
POSTGRES_PORT = 5432
POSTGRES_FULL_URL = f"{POSTGRES_URL}:{POSTGRES_PORT}"
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'twitter')
POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME', 'admin')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'admin')

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

API_QUEUE = 'API'


# -----------------------------------------------------------
# NEO4J
# -----------------------------------------------------------
NEO4J_URL = os.environ.get('NEO4J_URL', 'localhost')
NEO4J_PORT = 7687
NEO4J_FULL_URL = f"{NEO4J_URL}:{NEO4J_PORT}"
NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'neo4jPI')
