from wrappers.neo4j_wrapper import Neo4jAPI
from wrappers.rabbit_messaging import RabbitMessaging
from wrappers.rabbit_messaging import MessagingSettings
from credentials import TASKS_EXCHANGE, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, VHOST, RABBITMQ_FULL_HTTP_URL, \
	REST_API_EXCHANGE, REST_API_ROUTING_KEY
import os

NEO4J_PORT = os.environ.get('NEO4J_PORT', None)

if NEO4J_PORT:
	FULL_URL = f'neo4j:{NEO4J_PORT}'
	neo4j = Neo4jAPI(FULL_URL)
else:
	neo4j = Neo4jAPI()

messaging_settings = {
	TASKS_EXCHANGE: MessagingSettings(
		exchange=REST_API_EXCHANGE,
		routing_key=REST_API_ROUTING_KEY
	)
}

rabbit_client = RabbitMessaging(RABBITMQ_FULL_HTTP_URL, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, VHOST, messaging_settings)
