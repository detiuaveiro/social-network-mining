## @package twitter.bots
# coding: UTF-8

import logging
from typing import List, Union

import tweepy
from tweepy.error import TweepError
from tweepy.models import User, Status

import bots.messages_types as messages_types
from bots.rabbit_messaging import RabbitMessaging
from bots.settings import *
from bots.utils import *
from credentials import VHOST, LOG_EXCHANGE, LOG_ROUTING_KEY, DATA_EXCHANGE, QUERY_EXCHANGE, TASKS_EXCHANGE, \
	TASKS_QUEUE_PREFIX

logger = logging.getLogger("bot-agents")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("bot_agent.log", "w"))
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

	def __get_tweet_dict(self, tweet: Status):
		tweet_dict = tweet._json.copy()
		tweet_dict['user'] = tweet_dict['user']['id']
		return tweet_dict

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
		logger.debug(f"Sending {tweet} with message_type <{message_type.name}>")
		self.__send_data(self.__get_tweet_dict(tweet), message_type)

	def __send_data(self, data, message_type: messages_types.BotToServer):
		self.__send_message(data, message_type, DATA_EXCHANGE)

	def __send_query(self, data, message_type: messages_types.BotToServer):
		self.__send_message(data, message_type, QUERY_EXCHANGE)

	def __send_event(self, data, message_type: messages_types.BotToServer):
		self.__send_message(data, message_type, LOG_EXCHANGE)

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

		self._id = self._twitter_api.me().id
		logger.debug(f"Sending our user <{self._id}> to {DATA_EXCHANGE}")
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

			# ask to reply to tweet
			self.__send_tweet(tweet, messages_types.BotToServer.QUERY_TWEET_REPLY)

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

	def __follow_users(self, id_type: str, data: List[Union[str, int]]):
		"""Function to follow a specific group of users

		:param id_type: user's identification type (can have the value id (numerical identification), or screen_name
			(string identification)
		:param data: list of the user's identifications to follow
		"""
		logger.info("Starting follow users routine")

		if id_type == "id":
			id_type = "user_id"

		for user_id in data:
			logger.info(f"Searching for User object identified by [{id_type}] with <{user_id}>")

			try:
				arg_param = {
					id_type: user_id
				}
				user: User = self._twitter_api.get_user(**arg_param)

				if user:
					logger.info(f"Found user: {user}")
					self.__follow_user(user)
			except TweepError as error:
				logger.error(f"Unable to find user identified by [{id_type}] with <{user_id}>: {error}")

	def __follow_user(self, user: User):
		"""Function to follow a specific user. It sends the user to the server and then, if the bot doesn't follow the
			user, it tries to follow the user. At last, it reads the user's tweets timeline and sends it to the server

		:param user: user to follow
		"""
		logger.info(f"Following user <{user}>")

		self.__send_user(user)

		if not user.following:
			virtual_read_wait(user.description)

			try:
				user.follow()
				logger.info(f"Followed User with id <{user.id}>")
				self.__send_event(user._json, messages_types.BotToServer.EVENT_USER_FOLLOWED)
			except TweepError as error:
				if error.api_code == FOLLOW_USER_ERROR_CODE:
					logger.error(f"Unable to follow User with id <{user.id}>: {error}")
				else:
					logger.error(f"Error with api_code={error.api_code}: {error}")

		if not user.protected or (user.protected and user.following):
			self.__read_timeline(user, jump_users=True)

	def __find_tweet_by_id(self, tweet_id: int) -> Union[Status, None]:
		"""Function to find and return a tweet for a given id

		:param tweet_id: id of the tweet which we want to find
		"""
		try:
			return self._twitter_api.get_status(tweet_id)
		except TweepError as error:
			logger.error(f"Error finding tweet with id <{tweet_id}>: {error}")
			return None

	def __like_tweet(self, tweet_id: int):
		"""Function to like a tweet

		:param tweet_id: id of the tweet which we want to give a like
		"""
		logger.info("Starting like tweets routine")

		tweet: Status = self.__find_tweet_by_id(tweet_id)
		if tweet:
			# read the tweet
			read_time = virtual_read_wait(tweet.text)
			logger.debug(f"Read Tweet in {read_time}")
			try:
				if tweet.favorited:
					logger.info(f"Tweet with id <{tweet_id}> already liked, no need to like again")
				else:
					logger.info(f"Linking tweet with id <{tweet.id}>")
					tweet.favorite()
					self.__send_event(self.__get_tweet_dict(tweet), messages_types.BotToServer.EVENT_TWEET_LIKED)
			except Exception as error:
				logger.error(f"Error liking tweet with id <{tweet_id}>: {error}")

	def __retweet_tweet(self, tweet_id: id):
		"""Function to retweet a specific tweet, givem the id of that tweet

		:param tweet_id: id of the tweet we want to retweet
		"""
		logger.info("Starting routine retweet tweet...")

		tweet: Status = self.__find_tweet_by_id(tweet_id)
		if tweet:
			# read the tweet
			read_time = virtual_read_wait(tweet.text)
			logger.debug(f"Read Tweet in {read_time}")

			try:
				if tweet.retweeted:
					logger.info(f"Tweet with id <{tweet.id}> already retweeted, no need to retweet again")
				else:
					logger.info(f"Retweeting Tweet with id <{tweet.id}>")
					tweet.retweet()
					self.__send_event(self.__get_tweet_dict(tweet), messages_types.BotToServer.EVENT_TWEET_RETWEETED)
			except Exception as error:
				logger.error(f"Error retweeting tweet with id <{tweet_id}>: {error}")

	def __post_tweet(self, text: str, reply_id: int = None):
		"""Function to post a new tweet. This can or cannot be a reply to other tweet

		:param text: text to post in new tweet
		:param reply_id: tweet to reply to
		"""
		logger.info("Starting routine post tweet...")

		write_time = virtual_read_wait(text)
		logger.debug(f"Tweet take {write_time} seconds to be written")

		args = {
			'status': text,
			'auto_populate_reply_metadata': True
		}
		if reply_id:
			args['in_reply_to_status_id'] = reply_id

		try:
			tweet: Status = self._twitter_api.update_status(**args)
			self.__send_tweet(tweet, messages_types.BotToServer.SAVE_TWEET)

			if reply_id:
				self.__send_event(self.__get_tweet_dict(tweet), messages_types.BotToServer.EVENT_TWEET_REPLIED)

			logger.debug("Tweet posted with success")
		except TweepError as error:
			logger.error(f"Error posting a new tweet: {error}")

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
						logger.warning(f"Not processing {messages_types.ServerToBot.FIND_BY_KEYWORDS} with {task_params}")
					elif task_type == messages_types.ServerToBot.FOLLOW_USERS:
						self.__follow_users(id_type=task_params['type'], data=task_params['data'])
					elif task_type == messages_types.ServerToBot.LIKE_TWEETS:
						self.__like_tweet(task_params)
					elif task_type == messages_types.ServerToBot.RETWEET_TWEETS:
						self.__retweet_tweet(task_params)
					elif task_type == messages_types.ServerToBot.FIND_FOLLOWERS:
						pass
					elif task_type == messages_types.ServerToBot.POST_TWEET:
						self.__post_tweet(**task_params)
					else:
						logger.warning(f"Received unknown task type: {task_type}")
				else:
					logger.warning("There are not new messages on the tasks's queue")
					# TODO -> VER O QUE FAZER NESTA SITUAÇÃO
					wait(5)
			except Exception as error:
				logger.error(f"Error on bot's loop: {error}")
				# exit(1)
