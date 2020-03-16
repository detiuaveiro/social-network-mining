import logging
from typing import List, Dict, Union

import tweepy
from tweepy.error import TweepError
from tweepy.models import User, Status, ResultSet

import messages_types
from rabbit_messaging import RabbitMessaging, MessagingSettings
from settings import *
from utils import *

logger = logging.getLogger("bot-agents")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("bot_agens.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
logger.addHandler(handler)


class TwitterBot(RabbitMessaging):
	def __init__(self, url, username, password, vhost, messaging_settings, bot_id, api: tweepy.API):
		super().__init__(url, username, password, vhost, messaging_settings)
		self._id = bot_id
		self._twitter_api = api
		self.user: User
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

	def __send_message(self, data, message_type: messages_types.BotToServer, exchange):
		"""Function to send a new message to the server throw rabbitMQ

		:param data: data to send
		:param message_type: type of message to send to server
		:param exchange: rabbit's exchange where to send the new message
		"""
		self._send_message(to_json({
			'type': message_type,
			'bot_id': self._id,
			'timestamp': current_time(),
			'data': data
		}), exchange)

	def __send_user(self, user: User):
		"""Function to send a twitter's User object to the server

		:param user: user to send
		"""
		logger.debug(f"Sending {user}")
		self.__send_data(user._json, messages_types.BotToServer.SAVE_USER)

	def __send_tweet(self, tweet: Status, message_type: messages_types.BotToServer):
		logger.debug(f"Sending {tweet}")

		tweet_to_send = tweet._json.copy()
		tweet_to_send['user'] = tweet_to_send['user']['id']
		self.__send_data(tweet_to_send, message_type)

	def __send_data(self, data, message_type: messages_types.BotToServer):
		self.__send_message(data, message_type, DATA_EXCHANGE)

	def __send_query(self, data, message_type: messages_types.BotToServer):
		self.__send_message(data, message_type, QUERY_EXCHANGE)

	def __receive_message(self):
		"""Function to consume a new message from the tasks's queue
		"""
		return self._receive_message(TASKS_EXCHANGE)

	def __setup(self):
		"""Function to setting up messaging queues and check if twitter credentials are ok
		"""

		logger.debug("Setting up messaging")
		self._setup_messaging()

		logger.debug("Verifying credentials")
		try:
			self.user = self._twitter_api.verify_credentials()
			logger.info(f"Logged in as:{self.user}")
		except TweepError as error:
			logger.error(f"Error verifying credentials: {error}")
			exit(1)

		logger.debug(f"Sending our user to {DATA_EXCHANGE}")
		self.__send_user(self.user)

		logger.info("Reading home timeline")
		self.__read_timeline(self.user)

		# ver porque não está a dar (o twitter não está a deixar aceder)
		# self.__direct_messages()

	def __user_timeline_tweets(self, user: User, **kwargs) -> List[Status]:
		"""Function to get the 20 (default) most recent tweets (including retweets) from some user

		:param user: user whom tweets we want
		:param kwargs: dictionary with keyword arguments. These arguments can be the follows:
			- since_id: Returns only statuses with an ID greater than (that is, more recent than) the specified ID
    		- max_id: Returns only statuses with an ID less than (that is, older than) or equal to the specified ID
    		- count: Specifies the number of statuses to retrieve
    		- page: Specifies the page of results to retrieve. Note: there are pagination limits
		"""
		logger.debug(f"Getting timeline tweets for User with id={user.id}")
		if user.id == self.user.id:
			return list(self._twitter_api.home_timeline(**kwargs))
		return list(user.timeline(**kwargs))

	def __read_timeline(self, user: User, jump_users: bool = False, max_depth: int = 3, current_depth: int = 0):
		"""Function to get an user's timeline tweets. At the same time, this function send to the server requests to
			like a tweet, to retweet a tweet and also sends all users that made some tweet, but we don't know yet.
			Also, this function is recursive, and tries to get all this data to the new users it possibility find

		:param user: user object to read the timeline for
		:param jump_users: flag to know if we should jump between tweet's users or not
		:param max_depth: maximum recursion's depth
		:param current_depth: current recursion's depth (to control the depth of the function's recursion)
		"""
		if current_depth == max_depth:
			return

		logger.debug(f"Reading user's <{user.__str__()}> timeline")
		tweets = self.__user_timeline_tweets(user, count=MAX_NUMBER_TWEETS_RETRIEVE_TIMELINE)

		total_read_time = 0
		for tweet in tweets:
			self.__send_tweet(tweet, messages_types.BotToServer.SAVE_TWEET)

			total_read_time += virtual_read_wait(tweet.text)

			# If it's our own tweet, we don't really need to do any logic
			if self.user.id == tweet.user.id:
				continue

			# Processing the tweet regarding liking/retweeting
			if not tweet.favorited:
				self.__send_tweet(tweet, messages_types.BotToServer.QUERY_TWEET_LIKE)
			if not tweet.retweeted:
				self.__send_tweet(tweet, messages_types.BotToServer.QUERY_TWEET_RETWEET)

			if not jump_users:
				tweet_user = tweet.user
				self.__send_user(tweet_user)

				user_attributes = tweet_user.__dir__()

				if 'following' in user_attributes and tweet_user.protected and not tweet_user.following:
					logger.warning(f"Found user with ID={tweet_user.id} but he's protected and we're not "
								   f"following him, so can't read his timeline")
					continue
				elif 'suspended' in user_attributes and tweet_user.suspended:
					logger.warning(f"Found user with ID={tweet_user.id} but his account was suspended, "
								   f"so can't read his timeline")
					continue
				else:
					self.__read_timeline(tweet_user, jump_users=jump_users,
										 max_depth=max_depth, current_depth=current_depth + 1)
		logger.debug(f"Read {user.id}'s timeline in {total_read_time} seconds")

	def __direct_messages(self):
		logger.info("Checking direct messages")
		messages = self._twitter_api.list_direct_messages()
		self.__send_data(messages, messages_types.BotToServer.SAVE_DIRECT_MESSAGES)

	def run(self):
		"""Bot's loop. As simple as a normal handler, tries to get tasks from the queue and, depending on the
			task, does a different action
		"""
		self.__setup()

		while True:
			try:
				logger.info(f"Getting next task from {TASKS_QUEUE_PREFIX}")
				task = self.__receive_message()

				if task:
					task_type, task_params = task['type'], task['params']
					logger.debug(f"Received task <{task}>")

					if task_type == messages_types.ServerToBot.FIND_BY_KEYWORDS:
						pass
					elif task_type == messages_types.ServerToBot.LIKE_TWEETS:
						pass
					elif task_type == messages_types.ServerToBot.RETWEET_TWEETS:
						pass
					elif task_type == messages_types.ServerToBot.RETWEET_TWEETS:
						pass
					elif task_type == messages_types.ServerToBot.FIND_FOLLOWERS:
						pass
					elif task_type == messages_types.ServerToBot.POST_TWEET:
						pass
					else:
						logger.warning(f"Received unknown task type: {task_type}")
				else:
					logger.warning("There are not new messages on the tasks's queue")
					# TODO -> VER O QUE FAZER NESTA SITUAÇÃO
					wait(5)
			except Exception as error:
				logger.error(f"Error on bot's loop: {error}")
				exit(1)

	def __follow_users_routine(self, params: Dict[str, Union[str, List[Union[str, int]]]]):
		pass


if __name__ == "__main__":
	bot_id = 1103294806497902594

	messaging_settings = {
		TASKS_EXCHANGE: MessagingSettings(exchange=TASKS_EXCHANGE, routing_key=f"{TASKS_ROUTING_KEY_PREFIX}.{bot_id}",
										  queue=f"{TASKS_QUEUE_PREFIX}-{bot_id}"),
		LOG_EXCHANGE: MessagingSettings(exchange=LOG_EXCHANGE, routing_key=LOG_ROUTING_KEY),
		QUERY_EXCHANGE: MessagingSettings(exchange=QUERY_EXCHANGE, routing_key=QUERY_ROUTING_KEY),
		DATA_EXCHANGE: MessagingSettings(exchange=DATA_EXCHANGE, routing_key=DATA_ROUTING_KEY)
	}

	# consumer_key = "yqoymTNrS9ZDGsBnlFhIuw"
	# consumer_secret = "OMai1whT3sT3XMskI7DZ7xiju5i5rAYJnxSEHaKYvEs"
	# token = "1097916541830680576-RWAa8hM2tkGMXQWaa0Bg5sDYTFD0oV"
	# token_secret = "bYyREitpd1J1wr758FMwmk7TI5KHyMEomEv80jgecJUVL"
	consumer_key = "vP8ULCHpJYTcRRfNqiVHLLemC"
	consumer_secret = "e3C7OtUlMh3VxEi0Bx038bv9hCKwYGFgbH7dnsLNpvpUL4SWy4"
	token = "1103294806497902594-Q90yPSULqg27zcWjLSZ99ZSzgGyQYP"
	token_secret = "iaK1qYJEtYNAx5Npv90VZB0bkPjaLojOXD5HuJrZCAfsb"

	twitter_auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
	twitter_auth.set_access_token(key=token, secret=token_secret)
	bot = TwitterBot("localhost:15672", RABBIT_USERNAME, RABBIT_PASSWORD, VHOST, messaging_settings, bot_id,
					 tweepy.API(auth_handler=twitter_auth, wait_on_rate_limit=True))
	bot.run()
