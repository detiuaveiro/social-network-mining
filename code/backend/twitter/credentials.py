import os

# -----------------------------------------------------------
#  MONGO 
# -----------------------------------------------------------
MONGO_URL = os.environ['MONGO_URL']  # "localhost"
MONGO_PORT = 27017
MONGO_FULL_URL = f"{MONGO_URL}:{MONGO_PORT}"
MONGO_DB = os.environ['MONGO_DB']  # "twitter"
MONGO_USERNAME = os.environ['MONGO_USERNAME']  # "admin"
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']  # "admin"

# -----------------------------------------------------------
# POSTGRES 
# -----------------------------------------------------------
POSTGRES_URL = os.environ['POSTGRES_URL']  # "localhost"
POSTGRES_PORT = 5432
POSTGRES_FULL_URL = f"{POSTGRES_URL}:{POSTGRES_PORT}"
POSTGRES_DB = os.environ['POSTGRES_DB']  # "twitter"
POSTGRES_USERNAME = os.environ['POSTGRES_USERNAME']  # "admin"
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']  # "admin"

# -----------------------------------------------------------
# RABBITMQ
# -----------------------------------------------------------
RABBITMQ_URL = os.environ['RABBITMQ_URL']  # "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_FULL_URL = f"{RABBITMQ_URL}:{RABBITMQ_PORT}"
RABBITMQ_USERNAME = os.environ['RABBITMQ_USERNAME']  # "pi_rabbit_admin"
RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']  # "yPvawEVxks7MLg3lfr3g"
RABBITMQ_VHOST = "PI"

# Queues and Exchanges
TT_DATA_EXCHANGE = "twitter_data"
TT_TASK_DELIVER = "task_deliver"
TT_LOGS = 'logs'
TT_QUERIES = "queries"
DATA_RK = "data.twitter"
LOGS_RK = 'logs.twitter'
QUERIES_RK = 'queries.twitter'
API_QUEUE = 'API'

# -----------------------------------------------------------
# NEO4J
# -----------------------------------------------------------
NEO4J_URL = os.environ['RABBITMQ_PASSWORD']  # "localhost"
NEO4J_PORT = 7687
NEO4J_FULL_URL = f"{NEO4J_URL}:{NEO4J_PORT}"
NEO4J_USERNAME = os.environ['RABBITMQ_PASSWORD']  # "neo4j"
NEO4J_PASSWORD = os.environ['RABBITMQ_PASSWORD']  # "neo4jPI"
