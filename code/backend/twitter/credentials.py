# -----------------------------------------------------------
#  MONGO 
# -----------------------------------------------------------
# MONGO_URL = "192.168.85.46"
MONGO_URL = "localhost"
MONGO_PORT = 27017
MONGO_FULL_URL = f"{MONGO_URL}:{MONGO_PORT}"
MONGO_DB = "snm_mongo"


# -----------------------------------------------------------
# POSTGRES 
# -----------------------------------------------------------
# POSTGRES_URL = "192.168.85.46"
POSTGRES_URL = "localhost"
POSTGRES_PORT = 5432
POSTGRES_FULL_URL = f"{POSTGRES_URL}:{POSTGRES_PORT}"
#POSTGRES_POLICIES_DB = "snm_policies_pg"
#POSTGRES_ANALYSIS_DB = "snm_analysis_pg"
POSTGRES_DB = 'postgres'
POSTGRES_USERNAME = "snm"
POSTGRES_PASSWORD = "pg_snm"


# -----------------------------------------------------------
# RABBITMQ
# -----------------------------------------------------------
# RABBITMQ_URL = "192.168.85.185"
RABBITMQ_URL = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_FULL_URL = f"{RABBITMQ_URL}:{RABBITMQ_PORT}"
RABBITMQ_USERNAME = "pi_rabbit_admin"
RABBITMQ_VHOST = "PI"
RABBITMQ_PASSWORD = "yPvawEVxks7MLg3lfr3g"


# -----------------------------------------------------------
# NEO4J
# -----------------------------------------------------------
# NEO4J_URL = "192.168.85.187"
NEO4J_URL = "localhost"
NEO4J_PORT = 7687
NEO4J_FULL_URL = f"{NEO4J_URL}:{NEO4J_PORT}"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "neo4jPI"
