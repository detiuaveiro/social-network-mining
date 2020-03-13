import logging

import tweepy
from tweepy.error import TweepError

import messages_types
from rabbit_messaging import RabbitMessaging, MessagingSettings
from settings import *
from utils import *

logger = logging.getLogger("bot-agents")
logger.setLevel(logging.DEBUG)


class TwitterBot(RabbitMessaging):
	def __init__(self, url, username, password, vhost, messaging_settings, bot_id, api: tweepy.API):
		super().__init__(url, username, password, vhost, messaging_settings)
		self._id = bot_id
		self._twitter_api = api
		# self.user: User
		self._last_home_tweet: int = None

	def __repr__(self):
		return f"<TwitterBot id={self._id}, api={self._twitter_api}>"

	def __send_error_suspended_log(self, error: TweepError):
		logger.error(f"TweepyError with code=<{error.api_code}> and reason=<{error.reason}>: {error}")

		if error.api_code in ACCOUNT_SUSPENDED_ERROR_CODES:
			data = {
				"type": messages_types.BotToServer.EVENT_USER_SUSPENDED,
				"bot_id": self._id,
				"timestamp": current_time(),
				"data": {
					"code": error.api_code,
					"msg": error.reason
				},
			}

			self._messaging.publish(vhost=VHOST, xname=LOG_EXCHANGE, rt_key=LOG_ROUTING_KEY, payload=to_json(data))

	def __setup(self):
		"""Function to setting up messaging queues and check if twitter credentials are ok
		"""

		logger.debug("Setting up messaging")
		self._setup_messaging()

		logger.debug("Verifying credentials")
		self.user = self._twitter_api.verify_credentials()
		print(self.user)

	def run(self):
		self.__setup()


if __name__ == "__main__":
	messaging_settings = {
		'tasks': MessagingSettings(TASKS_EXCHANGE, TASKS_QUEUE_PREFIX, TASKS_ROUTING_KEY_PREFIX),
		'log': MessagingSettings(exchange=LOG_EXCHANGE, routing_key=LOG_ROUTING_KEY),
		'query': MessagingSettings(exchange=QUERY_EXCHANGE, routing_key=QUERY_ROUTING_KEY),
		'data': MessagingSettings(exchange=DATA_EXCHANGE, routing_key=DATA_ROUTING_KEY)
	}

	consumer_key = "yqoymTNrS9ZDGsBnlFhIuw"
	consumer_secret = "OMai1whT3sT3XMskI7DZ7xiju5i5rAYJnxSEHaKYvEs"
	token = "1097916541830680576-RWAa8hM2tkGMXQWaa0Bg5sDYTFD0oV"
	token_secret = "bYyREitpd1J1wr758FMwmk7TI5KHyMEomEv80jgecJUVL"

	twitter_auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
	twitter_auth.set_access_token(key=token, secret=token_secret)
	bot = TwitterBot("localhost:15672", RABBIT_USERNAME, RABBIT_PASSWORD, VHOST, messaging_settings, 1,
					 tweepy.API(auth_handler=twitter_auth, wait_on_rate_limit=True))
	bot.run()
