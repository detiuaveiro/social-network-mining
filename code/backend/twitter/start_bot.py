from bots.settings import *
from bots.rabbit_messaging import MessagingSettings
import tweepy
from bots.twitter_bot import TwitterBot


if __name__ == "__main__":
	bot_id = 1103294806497902594

	messaging_settings = {
		TASKS_EXCHANGE: MessagingSettings(exchange=TASKS_EXCHANGE, routing_key=f"{TASKS_ROUTING_KEY_PREFIX}.{bot_id}",
										  queue=f"{TASKS_QUEUE_PREFIX}-{bot_id}"),
		LOG_EXCHANGE: MessagingSettings(exchange=LOG_EXCHANGE, routing_key=LOG_ROUTING_KEY),
		QUERY_EXCHANGE: MessagingSettings(exchange=QUERY_EXCHANGE, routing_key=QUERY_ROUTING_KEY),
		DATA_EXCHANGE: MessagingSettings(exchange=DATA_EXCHANGE, routing_key=DATA_ROUTING_KEY)
	}

	consumer_key = "vP8ULCHpJYTcRRfNqiVHLLemC"
	consumer_secret = "e3C7OtUlMh3VxEi0Bx038bv9hCKwYGFgbH7dnsLNpvpUL4SWy4"
	token = "1103294806497902594-Q90yPSULqg27zcWjLSZ99ZSzgGyQYP"
	token_secret = "iaK1qYJEtYNAx5Npv90VZB0bkPjaLojOXD5HuJrZCAfsb"

	twitter_auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
	twitter_auth.set_access_token(key=token, secret=token_secret)
	bot = TwitterBot("localhost:15672", RABBIT_USERNAME, RABBIT_PASSWORD, VHOST, messaging_settings, bot_id,
					 tweepy.API(auth_handler=twitter_auth, wait_on_rate_limit=True))
	bot.run()
