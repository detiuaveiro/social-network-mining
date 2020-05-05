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
		self._name: str = 'bot'
		self._screen_name: str = 'bot'
		self._id_str: str = None
		self._id = bot_id
		self._twitter_api: tweepy.API = api
		self.user: User

	def __repr__(self):
		return f"<TwitterBot id={self._id}, api={self._twitter_api}>"

	def __send_error_suspended_log(self, error: TweepError):
		logger.exception(f"TweepyError <{error}> with code=<{error.api_code}> and reason=<{error.reason}>: ")

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

	@staticmethod
	def __get_tweet_dict(tweet: Status):
		tweet_dict = tweet._json.copy()
		# tweet_dict['user'] = tweet_dict['user']['id']
		return tweet_dict

	def __send_message(self, data, message_type: messages_types.BotToServer, exchange):
		"""Function to send a new message to the server through rabbitMQ

		:param data: data to send
		:param message_type: type of message to send to server
		:param exchange: rabbit's exchange where to send the new message
		"""

		self._send_message(to_json({
			'type': message_type,
			'bot_id': self._id,
			'bot_id_str': self._id_str,
			'bot_name': self._name,
			'bot_screen_name': self._screen_name,
			'timestamp': current_time(),
			'data': data
		}), exchange)

	def __send_request_follow(self, user: User):
		"""Function to send a follow user request

		:param user:  user to send
		:return:
		"""
		logger.debug(f"Sending request follow to {user.id} ")
		tweets = []
		if not user._json['protected']:
			tweets = [tweet._json for tweet in self.__user_timeline_tweets(user, tweet_mode="extended")]

		self.__send_data({
			'user': user._json,
			'tweets': tweets
		}, messages_types.BotToServer.QUERY_FOLLOW_USER)

	def __send_user(self, user: User, message_type: messages_types.BotToServer):
		"""Function to send a twitter's User object to the server

		:param user: user to send
		"""
		logger.debug(f"Sending {user.id} with message type {message_type}")
		self.__send_data(user._json, message_type)

	def __send_tweet(self, tweet: Status, message_type: messages_types.BotToServer):
		logger.debug(f"Sending {tweet.id} with message_type <{message_type.name}>")
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

			self._name = self._twitter_api.me().name
			self._screen_name = self._twitter_api.me().screen_name
			self._id_str = self._twitter_api.me().id_str
		except TweepError as error:
			logger.exception(f"Error {error} verifying credentials:")
			exit(1)

		logger.debug(f"Sending our user <{self._id}> to {DATA_EXCHANGE}")
		self.__send_user(self.user, messages_types.BotToServer.SAVE_USER)

		logger.info(f"Sending the last 200 followers of our bot")
		self.__get_followers(user_id=self._id_str)

		logger.info("Reading home timeline")
		self.__read_timeline(self.user)

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

		logger.debug(f"Reading user's <{user.id}> timeline")
		tweets = self.__user_timeline_tweets(user, count=MAX_NUMBER_TWEETS_RETRIEVE_TIMELINE, tweet_mode="extended")

		total_read_time = self.__interpret_tweets(tweets, jump_users, max_depth, current_depth)
		logger.debug(f"Read {user.id}'s timeline in {total_read_time} seconds")

	def __search_tweets(self, keywords: list, language: str = 'pt', max_keywords: int = 3):
		logger.info(f"Starting to search for tweets for keywords {keywords}")

		total_read_time = 0
		for i in range(max_keywords):
			if len(keywords) > 0:
				keyword = random.choice(keywords)
				keywords.remove(keyword)

				# TODO -> 100 is the maximum number of tweets per page -> if we have time we can add pagination and
				#  obtain more tweets
				# get tweets in portuguese and from Portugal (center of Portugal and a radius equal form the center
				# to the most distant point)
				tweets = self._twitter_api.search(q=keyword, lang=language, geocode="39.557191,-8.1,300km",
				                                  tweet_mode="extended", count=100)
				total_read_time += self.__interpret_tweets(tweets, max_depth=2)

		logger.debug(f"Search completed in {total_read_time} seconds")

	def __interpret_tweets(self, tweets, jump_users: bool = False, max_depth: int = 3, current_depth: int = 0) -> float:

		total_read_time = 0
		for tweet in tweets:
			self.__send_tweet(tweet, messages_types.BotToServer.SAVE_TWEET)

			total_read_time += virtual_read_wait(tweet.full_text if 'full_text' in tweet._json else tweet.text)

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
				logger.info("Starting to read tweet's author")

				tweet_user = tweet.user
				self.__send_user(tweet_user, messages_types.BotToServer.SAVE_USER)

				user_attributes = tweet_user.__dir__()

				logger.debug(
					f"Tweet with author info {tweet_user.following if 'following' in user_attributes else 'nothing'}")
				if 'following' in user_attributes and not tweet_user.following or 'following' not in user_attributes:
					logger.debug(f"Requesting to follow user {tweet_user.id}")
					self.__send_request_follow(tweet_user)

				if 'following' in user_attributes and tweet_user.protected and not tweet_user.following:
					logger.warning(f"Found user with ID={tweet_user.id} but he's protected and we're not "
								   f"following him, so can't read his timeline")

				elif 'suspended' in user_attributes and tweet_user.suspended:
					logger.warning(f"Found user with ID={tweet_user.id} but his account was suspended, "
								   f"so can't read his timeline")
				else:
					self.__read_timeline(tweet_user, jump_users=jump_users,
										 max_depth=max_depth, current_depth=current_depth + 1)
		return total_read_time

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
					logger.info(f"Found user: {user.id}")
					self.__follow_user(user)
			except TweepError as error:
				logger.exception(f"Unable to find user identified by [{id_type}] with <{user_id}> because of error "
								 f"<{error}>:")

	def __follow_user(self, user: User):
		"""Function to follow a specific user. It sends the user to the server and then, if the bot doesn't follow the
			user, it tries to follow the user. At last, it reads the user's tweets timeline and sends it to the server

		:param user: user to follow
		"""
		logger.info(f"Following user <{user.id}>")

		if not user.following:
			virtual_read_wait(user.description)

			try:
				user.follow()
				logger.info(f"Followed User with id <{user.id}>")
				self.__send_user(user, messages_types.BotToServer.SAVE_USER)
			except TweepError as error:
				if error.api_code == FOLLOW_USER_ERROR_CODE:
					logger.exception(f"Unable to follow User with id <{user.id}> because of error <{error}>: ")
				else:
					logger.exception(f"Error <{error}> with api_code={error.api_code}: ")

		if not user.protected or (user.protected and user.following):
			self.__read_timeline(user, jump_users=False, max_depth=3)

	def __get_followers(self, user_id: int):
		"""
		Function to get follower of some user

		Note: for now, it just gets the last 200 followers per user. TODO -> get all users maybe
		:param user_id: user's id of whom we want to get the followers
		"""
		logger.info(f"Start to get the followers of user with id {user_id}")
		followers = self._twitter_api.followers(id=user_id, count=200)

		logger.info(f"Sending followers of user {user_id} to the control center")
		self.__send_data({
			'id': user_id,
			'followers': [follower._json for follower in followers]
		}, messages_types.BotToServer.SAVE_FOLLOWERS)

	def __get_user_dict(self, user_id: int):
		"""Function to get the full user object by its id, and send it to the control center
		:param user_id: id of the user we want to send to the control center
		"""
		logger.info(f"Getting user of id {user_id}")

		try:
			self.__send_user(self._twitter_api.get_user(user_id), messages_types.BotToServer.SAVE_USER)
		except TweepError as error:
			logger.exception(f"Error <{error}> finding user with id <{user_id}>: ")
			return None

	def __get_tweet_by_id(self, tweet_id: int):
		"""
		Function to get the full tweet object by its id, and send it to the control center
		:param tweet_id: id of the tweet we want to send to the control center
		"""

		logger.info(f"Getting tweet of id {tweet_id}")
		self.__send_tweet(self.__find_tweet_by_id(tweet_id), messages_types.BotToServer.SAVE_TWEET)

	def __find_tweet_by_id(self, tweet_id: int) -> Union[Status, None]:
		"""Function to find and return a tweet for a given id

		:param tweet_id: id of the tweet which we want to find
		"""
		try:
			return self._twitter_api.get_status(tweet_id)
		except TweepError as error:
			logger.exception(f"Error <{error}> finding tweet with id <{tweet_id}>: ")
			return None

	def __like_tweet(self, tweet_id: int):
		"""Function to like a tweet

		:param tweet_id: id of the tweet which we want to give a like
		"""
		logger.info("Starting like tweets routine")

		tweet: Status = self.__find_tweet_by_id(tweet_id)
		if tweet:
			# read the tweet
			read_time = virtual_read_wait(tweet.full_text if 'full_text' in tweet._json else tweet.text)
			logger.debug(f"Read Tweet in {read_time}")
			try:
				if tweet.favorited:
					logger.info(f"Tweet with id <{tweet_id}> already liked, no need to like again")
				else:
					logger.info(f"Linking tweet with id <{tweet.id}>")
					tweet.favorite()
					self.__send_event(self.__get_tweet_dict(tweet), messages_types.BotToServer.EVENT_TWEET_LIKED)
			except Exception as error:
				logger.exception(f"Error <{error}> liking tweet with id <{tweet_id}>: ")

	def __retweet_tweet(self, tweet_id: id):
		"""Function to retweet a specific tweet, givem the id of that tweet

		:param tweet_id: id of the tweet we want to retweet
		"""
		logger.info("Starting routine retweet tweet...")

		tweet: Status = self.__find_tweet_by_id(tweet_id)
		if tweet:
			# read the tweet
			read_time = virtual_read_wait(tweet.full_text if 'full_text' in tweet._json else tweet.text)
			logger.debug(f"Read Tweet in {read_time}")

			try:
				if tweet.retweeted:
					logger.info(f"Tweet with id <{tweet.id}> already retweeted, no need to retweet again")
				else:
					logger.info(f"Retweeting Tweet with id <{tweet.id}>")
					retweet: Status = self._twitter_api.retweet(id=tweet.id)
					logger.debug(f"Retweet: {retweet}")
					self.__send_tweet(retweet, messages_types.BotToServer.SAVE_TWEET)
					# self.__send_event(self.__get_tweet_dict(tweet), messages_types.BotToServer.EVENT_TWEET_RETWEETED)
			except Exception as error:
				logger.exception(f"Error <{error}> retweeting tweet with id <{tweet_id}>: ")

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
			# if reply_id:
			#	self.__send_event(self.__get_tweet_dict(tweet), messages_types.BotToServer.EVENT_TWEET_REPLIED)

			logger.debug("Tweet posted with success")
		except TweepError as error:
			logger.exception(f"Error {error} posting a new tweet: ")

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
					logger.debug(f"Received task of type {messages_types.ServerToBot(task_type).name}: {task_params}")

					if task_type == messages_types.ServerToBot.FIND_BY_KEYWORDS:
						logger.warning(
							f"Not processing {messages_types.ServerToBot.FIND_BY_KEYWORDS} with {task_params}")
					elif task_type == messages_types.ServerToBot.FOLLOW_USERS:
						self.__follow_users(id_type=task_params['type'], data=task_params['data'])
					elif task_type == messages_types.ServerToBot.LIKE_TWEETS:
						self.__like_tweet(task_params)
					elif task_type == messages_types.ServerToBot.RETWEET_TWEETS:
						self.__retweet_tweet(task_params)
					elif task_type == messages_types.ServerToBot.FIND_FOLLOWERS:
						logger.info(f"The bot was asked to get the followers for user with id <{task_params}>")
						self.__get_followers(user_id=task_params)
					# elif task_type == messages_types.ServerToBot.POST_TWEET:
					# 	self.__post_tweet(**task_params)
					elif task_type == messages_types.ServerToBot.KEYWORDS:
						self.__search_tweets(keywords=task_params)
					elif task_type == messages_types.ServerToBot.GET_TWEET_BY_ID:
						self.__get_tweet_by_id(tweet_id=task_params)
					elif task_type == messages_types.ServerToBot.GET_USER_BY_ID:
						self.__get_user_dict(user_id=task_params)
					else:
						logger.warning(f"Received unknown task type: {task_type}")
				else:
					logger.warning("There are not new messages on the tasks's queue")

					logger.info("Update the control center with the users who follow us")
					self.__get_followers(user_id=self._id_str)

					logger.info("Ask control center for keywords to search new tweets")
					self.__send_user(self._twitter_api.me(), messages_types.BotToServer.QUERY_KEYWORDS)
					wait(2)
			except Exception as error:
				logger.exception(f"Error {error} on bot's loop: ")
			# exit(1)
