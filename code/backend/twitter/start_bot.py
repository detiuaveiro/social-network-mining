## @package twitter

import os

from bots.rabbit_messaging import MessagingSettings
import tweepy
from bots.twitter_bot import TwitterBot
from credentials import TASKS_EXCHANGE, TASKS_ROUTING_KEY_PREFIX, TASKS_QUEUE_PREFIX, LOG_EXCHANGE, LOG_ROUTING_KEY, \
	QUERY_EXCHANGE, QUERY_ROUTING_KEY, DATA_EXCHANGE, DATA_ROUTING_KEY, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, VHOST, \
	RABBITMQ_FULL_HTTP_URL

if __name__ == "__main__":
	bot_id = int(os.environ.get('BOT_ID'))

	messaging_settings = {
		TASKS_EXCHANGE: MessagingSettings(exchange=TASKS_EXCHANGE, routing_key=f"{TASKS_ROUTING_KEY_PREFIX}.{bot_id}",
										  queue=f"{TASKS_QUEUE_PREFIX}-{bot_id}"),
		LOG_EXCHANGE: MessagingSettings(exchange=LOG_EXCHANGE, routing_key=LOG_ROUTING_KEY),
		QUERY_EXCHANGE: MessagingSettings(exchange=QUERY_EXCHANGE, routing_key=QUERY_ROUTING_KEY),
		DATA_EXCHANGE: MessagingSettings(exchange=DATA_EXCHANGE, routing_key=DATA_ROUTING_KEY)
	}

	consumer_key = os.environ.get('CONSUMER_KEY', '')
	consumer_secret = os.environ.get('CONSUMER_SECRET', '')
	token = os.environ.get('TOKEN', '')
	token_secret = os.environ.get('TOKEN_SECRET', '')
	proxy = os.environ.get('PROXY', 'socks5h://localhost:9050')

	twitter_auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
	twitter_auth.set_access_token(key=token, secret=token_secret)
	bot = TwitterBot(RABBITMQ_FULL_HTTP_URL, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, VHOST, messaging_settings, bot_id,
					 tweepy.API(auth_handler=twitter_auth, wait_on_rate_limit=True, proxy=proxy))
	bot.run()
