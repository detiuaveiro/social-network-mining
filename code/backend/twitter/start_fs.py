## @package twitter

import os

from follow_service.service import Service
from rabbit_messaging import MessagingSettings
from credentials import RABBITMQ_USERNAME, RABBITMQ_PASSWORD, VHOST, RABBITMQ_FULL_HTTP_URL, TASK_FOLLOW_QUEUE, \
	TASK_FOLLOW_EXCHANGE, TASK_FOLLOW_ROUTING_KEY_PREFIX, SERVICE_QUERY_EXCHANGE, SERVICE_QUERY_ROUTING_KEY

if __name__ == "__main__":
    messaging_settings = {
        TASK_FOLLOW_EXCHANGE: MessagingSettings(exchange=TASK_FOLLOW_EXCHANGE, routing_key=TASK_FOLLOW_ROUTING_KEY_PREFIX,
                                                queue=TASK_FOLLOW_QUEUE),
        SERVICE_QUERY_EXCHANGE: MessagingSettings(exchange=SERVICE_QUERY_EXCHANGE, routing_key=SERVICE_QUERY_ROUTING_KEY)
    }

    # consumer_key = os.environ.get('CONSUMER_KEY', '')
    # consumer_secret = os.environ.get('CONSUMER_SECRET', '')
    # token = os.environ.get('TOKEN', '')
    # token_secret = os.environ.get('TOKEN_SECRET', '')
    # proxy = os.environ.get('PROXY', 'socks5h://localhost:9050')

    service = Service(RABBITMQ_FULL_HTTP_URL, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, VHOST, messaging_settings)
    service.run()
