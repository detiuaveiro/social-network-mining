import json
import logging
import random

import pytz
from datetime import timedelta, datetime
import redis

from control_center.text_generator import ParlaiReplier
from control_center.translator_utils import Translator
from control_center.utils import tweet_to_simple_text

from control_center.policies_types import PoliciesTypes
from control_center.PEP import PEP
from messages_types import ServerToBot, BotToServer, ServerToFollowService, FollowServiceToServer

import log_actions
import neo4j_labels
from control_center import mongo_utils

from credentials import PARLAI_URL, PARLAI_PORT, TASKS_ROUTING_KEY_PREFIX, TASKS_QUEUE_PREFIX, TASK_FOLLOW_QUEUE, \
	TASK_FOLLOW_ROUTING_KEY_PREFIX, SERVICE_QUERY_EXCHANGE, REDIS_URL, REDIS_PORT
from wrappers.mongo_wrapper import MongoAPI
from wrappers.neo4j_wrapper import Neo4jAPI
from wrappers.postgresql_wrapper import PostgresAPI
import api.signal

log = logging.getLogger('Database Writer')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("control_center.log", "a"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)

PROBABILITY_SEARCH_KEYWORD = 0.000001
OBJECT_TTL = 300 #Object id will be in redis for 60s


class Control_Center:
	"""
	Class to simulate the behaviour of a bot:
	On receiving a message from a message broker, this class will act accordingly
	"""

	def __init__(self, rabbit_wrapper):
		"""
		This will start instaces for all the DB's API
		"""
		log.info("Control center initiated")

		self.postgres_client = PostgresAPI()
		self.mongo_client = MongoAPI()
		self.neo4j_client = Neo4jAPI()
		self.redis_client = redis.Redis(host=REDIS_URL, port=REDIS_PORT)
		self.pep = PEP()
		self.__utc = pytz.UTC

		# replier tools
		self.replier = ParlaiReplier(PARLAI_URL, PARLAI_PORT)
		self.translator = Translator()

		# rabbit vars
		self.rabbit_wrapper = rabbit_wrapper
		self.exchange = None
		self.deliver_tag = None
		self.channel = None

		# messages to send to old bot
		self.old_bot = None
		self.messages_to_send = []

		log.info(f"Control center configured: <{self.__dict__}>")

	def action(self, message):
		try:
			if self.exchange == SERVICE_QUERY_EXCHANGE:
				self.follow_service_action(message)
			else:
				self.bot_action(message)
		except Exception as error:
			log.exception(f"Error <{error}> on consuming new message: ")

	def bot_action(self, messages):
		for message in messages:
			message_type = message['type']
			log.info(f"Received new action from bot: {message['bot_id']} wants to do {BotToServer(message_type).name}")

			# search for keyword tweets time to time
			if random.random() < PROBABILITY_SEARCH_KEYWORD:
				log.info(f"Random sending a request to search for tweets of keywords to bot with id <{message['bot_id']}>")
				self.__send_keywords(message)

			if message_type == BotToServer.EVENT_TWEET_LIKED:
				self.__like_tweet_log(message)

			elif message_type == BotToServer.QUERY_TWEET_LIKE:
				self.request_tweet_like(message)

			elif message_type == BotToServer.QUERY_TWEET_RETWEET:
				self.request_retweet(message)

			elif message_type == BotToServer.QUERY_TWEET_REPLY:
				self.__request_tweet_reply(message)

			elif message_type == BotToServer.QUERY_FOLLOW_USER:
				self.__request_follow_user(message)

			elif message_type == BotToServer.SAVE_USER:
				if isinstance(message, dict):
					message = [message]
				self.save_user(message)

			elif message_type == BotToServer.SAVE_TWEET:
				log.info("Saving " + str(message))
				if isinstance(message, dict):
					message = [message]
				self.save_tweet(message)

			elif message_type == BotToServer.SAVE_DIRECT_MESSAGES:
				if isinstance(message, dict):
					message = [message]
				self.save_dm(message)

			elif message_type == BotToServer.EVENT_ERROR:
				self.error(message)

			elif message_type == BotToServer.SAVE_FOLLOWERS:
				self.__add_followers(message)

			elif message_type == BotToServer.QUERY_KEYWORDS:
				self.__send_keywords(message)

		log.info("Finished processing all messages")
		self.__save_dbs()
		self.__force_send()

	def follow_service_action(self, message):
		message_type = message['type']
		log.info(
			f"Received new action from follow_user service: Wants to do {FollowServiceToServer(message_type).name}")

		if message_type == FollowServiceToServer.REQUEST_POLICIES:
			self.__all_policies()
		elif message_type == FollowServiceToServer.FOLLOW_USER:
			self.__follow_user(message)
		elif message_type == FollowServiceToServer.CHANGE_EMAIL_STATUS:
			self.__change_email_status()

	def __change_email_status(self):
		log.debug("Changing email status")
		updated_notifications = self.postgres_client.update_notifications_status()
		if updated_notifications['success']:
			log.debug("Email status changed with success")
		else:
			log.error(f"Email status changed not committed due to the error -> {updated_notifications['error']}")

	def __all_policies(self):
		log.debug("Obtaining all policies available")
		policies = self.postgres_client.search_policies()
		if policies['success']:
			log.debug("Success obtaining all policies available")

			activated_notifications = self.postgres_client.search_notifications({"status": True})
			if not activated_notifications['success']:
				activated_notifications = []
			else:
				activated_notifications = activated_notifications['data']

			self.send_to_follow_user_service(ServerToFollowService.POLICIES_KEYWORDS, {
				'data': policies['data'],
				'activated_notifications': activated_notifications
			})
		else:
			log.error("Error obtaining all policies available")

	# Need DB API now
	def __find_followers(self, user1_id, user2_id):
		"""
		Action to follow user:
				Calls neo4j to add new relation between user (bot or normal user) and user
				Calls postgres_stats to add new log with the action details
		"""
		log.debug(f"User {user1_id} is following {user2_id}")
		type1 = self.__user_type(user1_id)
		type2 = self.__user_type(user2_id)

		relationship = {
			"id_1": user1_id,
			"id_2": user2_id,
			"type_1": type1,
			"type_2": type2
		}

		if self.neo4j_client.check_follow_exists(relationship):
			log.debug(f"User {user1_id} already follows the user {user2_id}")
			return
		self.neo4j_client.add_follow_relationship(relationship)

		if type1 == "Bot" or type2 == "Bot":
			bot_id, user_id = (user1_id, user2_id) if type1 == "Bot" else (user2_id, user1_id)

			self.postgres_client.insert_log({
				"bot_id": int(bot_id),
				"action": log_actions.FOLLOW,
				"target_id": int(user_id)
			})
			log.info(f"Bot {bot_id} successfully followed the user (or bot) {user_id}")

			# if the bot is following a user, we ask the bot to get the followers of that user
			log.info(f"Asking bot with id <{bot_id}> to get the followers of the user with id {user_id}")
			self.send(bot_id, ServerToBot.FIND_FOLLOWERS, user_id)

		log.info("Saved follow relation with success")

	def __like_tweet_log(self, data):
		"""
		Action to like tweet:
				Calls postgres_stats to add new log

		@param data dict with the bot id and the tweet he liked
		"""
		result = self.postgres_client.insert_log({
			"bot_id": int(data["bot_id_str"]),
			"action": log_actions.TWEET_LIKE,
			"target_id": int(data['data']['id_str'])
		})
		if result['success']:
			log.debug(f"Bot {data['bot_id']} liked tweet {data['data']['id']}")
		else:
			log.debug(f"Bot {data['bot_id']} could not like tweet {data['data']['id']}")
			log.error(f"Bot like caused error {result['error']}")

	def __retweet_log(self, data):
		"""
		Action to retweet:
				Calls postgres_stats to add new log

		@param data: dict containing bot and the tweet he retweeted
		"""
		result = self.postgres_client.insert_log({
			"bot_id": int(data["bot_id"]),
			"action": log_actions.RETWEET,
			"target_id": int(data['target_id'])
		})
		if result['success']:
			log.debug(f"Bot {data['bot_id']} retweeted {data['target_id']}")
		else:
			log.debug(f"Bot {data['bot_id']} could not retweet tweet {data['target_id']}")
			log.error(f"Bot like caused error {result['error']}")

	def __reply_tweet_log(self, data):
		"""
		Action to reply a tweet:
				Calls progres_stats to add what the bot replied and to which tweet

		@param data: dict contaning bot and the reply they made
		"""
		result = self.postgres_client.insert_log({
			"bot_id": int(data["bot_id"]),
			"action": log_actions.TWEET_REPLY,
			"target_id": int(data['target_id'])
		})
		if result['success']:
			log.debug(f"Bot {data['bot_id']} replied with {data['target_id']}")
		else:
			log.debug(f"Bot {data['bot_id']} could not reply with {data['target_id']}")
			log.error(f"Bot like caused error {result['error']}")

	def __quote_tweet_log(self, data):
		"""
		Action to reply a tweet:
				Calls postgres_stats to add what the bot replied and to which tweet

		@param data: dict contaning bot and the reply they made
		"""
		result = self.postgres_client.insert_log({
			"bot_id": int(data["bot_id"]),
			"action": log_actions.TWEET_QUOTE,
			"target_id": int(data['target_id'])
		})
		if result['success']:
			log.debug(f"Bot {data['bot_id']} replied with {data['target_id']}")
		else:
			log.debug(f"Bot {data['bot_id']} could not reply with {data['target_id']}")
			log.error(f"Bot like caused error {result['error']}")

	def __found_in_logs(self, bot=None, action=None, target=None, max_number_hours=1):
		"""
		Function to check if an action is already found in logs recently, therefore not being necessary to be done

		@param bot: id of bot who's requesting an action
		@param action: action the bot wants to take
		@param target: id of target that bot wants to take action to
		@return Boolean value confirming it found the log recently
		"""
		params = {}

		if bot:
			params['bot_id'] = bot
		if action:
			params['action'] = action
		if target:
			params['target_id'] = target
		if max_number_hours:
			params['timestamp'] = datetime.now() - timedelta(hours=max_number_hours)

		bot_logs = self.postgres_client.search_logs(params=params, limit=1)

		log.debug("Found the logs in the database")
		return bot_logs["success"] and len(bot_logs['data']) > 0

	def request_tweet_like(self, data):
		"""
		Action to request a like on tweeter:
				Calls the PEP to request a like
				Adds the log to postgres_stats, for the request and its result
				The result is based on the PDP methods

		@param data: dict containing the bot id and the tweet id
		"""
		log.info(f"Bot {data['bot_id']} requests a like to tweet {data['data']['id']}")
		if self.__found_in_logs(data["bot_id_str"], log_actions.LIKE_REQ, data['data']['id_str']):
			log.info("Action was already requested recently")
			return

		self.postgres_client.insert_log({
			"bot_id": int(data["bot_id_str"]),
			"action": log_actions.LIKE_REQ,
			"target_id": int(data['data']['id_str'])
		})

		request_accepted = self.pep.receive_message({
			"type": PoliciesTypes.REQUEST_TWEET_LIKE,
			"bot_id": data['bot_id'],
			"bot_id_str": data['bot_id_str'],
			"user_id": data['data']['user']['id'],
			"user_id_str": data['data']['user']['id_str'],
			"tweet_id": data['data']['id'],
			"tweet_id_str": data['data']['id_str'],
			"tweet_text": data['data']['full_text'] if 'full_text' in data['data'] else data['data']['text'],
			"tweet_entities": data['data']['entities']
		})

		if request_accepted:
			log.info(f"Bot {data['bot_id']} request accepted to like a tweet {data['data']['id']}")
			self.postgres_client.insert_log({
				"bot_id": int(data["bot_id_str"]),
				"action": log_actions.LIKE_REQ_ACCEPT,
				"target_id": int(data['data']['id_str'])
			})
			self.send(
				data['bot_id'], ServerToBot.LIKE_TWEETS,
				data['data']['id']
			)
		else:
			log.warning(f"Bot {data['bot_id']} request denied to like a tweet {data['data']['id']}")
			self.postgres_client.insert_log({
				"bot_id": int(data["bot_id_str"]),
				"action": log_actions.LIKE_REQ_DENY,
				"target_id": int(data['data']['id_str'])
			})

	def request_retweet(self, data):
		"""
		Action to request a retweet:
				Calls the PEP to request the retweet
				Adds the log to postgres_stats, for the request and its result
				The result is based on the PDP methods

		@param data: dict containing the bot id and the tweet id
		"""
		log.info(f"Bot {data['bot_id']} requests a retweet {data['data']['id']}")
		if self.__found_in_logs(data["bot_id_str"], log_actions.RETWEET_REQ, data['data']['id_str']):
			log.info("Action was already requested recently")
			return

		self.postgres_client.insert_log({
			"bot_id": int(data["bot_id_str"]),
			"action": log_actions.RETWEET_REQ,
			"target_id": int(data['data']['id_str'])
		})
		request_accepted = self.pep.receive_message({
			"type": PoliciesTypes.REQUEST_TWEET_RETWEET,
			"bot_id": data['bot_id'],
			"bot_id_str": data['bot_id_str'],
			"user_id": data['data']['user']['id'],
			"user_id_str": data['data']['user']['id_str'],
			"tweet_id": data['data']['id'],
			"tweet_id_str": data['data']['id_str'],
			"tweet_text": data['data']['full_text'] if 'full_text' in data['data'] else data['data']['text'],
			"tweet_entities": data['data']['entities']
		})

		if request_accepted:
			log.info(f"Bot {data['bot_id']} request accepted to retweet {data['data']['id']}")
			self.postgres_client.insert_log({
				"bot_id": int(data["bot_id_str"]),
				"action": log_actions.RETWEET_REQ_ACCEPT,
				"target_id": int(data['data']['id_str'])
			})
			self.send(
				data['bot_id'],
				ServerToBot.RETWEET_TWEETS, data['data']['id']
			)
		else:
			log.warning(f"Bot {data['bot_id']} request denied to retweet {data['data']['id']}")
			self.postgres_client.insert_log({
				"bot_id": int(data["bot_id_str"]),
				"action": log_actions.RETWEET_REQ_DENY,
				"target_id": int(data['data']['id_str'])
			})

	def __request_tweet_reply(self, data: dict):
		"""
		Action to request a reply:
				Calls the control center to request the reply
				Adds the log to postgres_stats, for the request and its result
				The result is based on the Policy API object

		@param data: dict containing the bot id and the tweet id
		"""
		tweet: dict = data['data']
		log.info(f"Bot {data['bot_id']} requests a reply {tweet['id']}")

		if self.__found_in_logs(data["bot_id"], log_actions.REPLY_REQ, tweet['id']):
			log.info("Action was already requested recently")
			return

		self.postgres_client.insert_log({
			"bot_id": int(data["bot_id_str"]),
			"action": log_actions.REPLY_REQ,
			"target_id": int(tweet['id_str'])
		})

		request_accepted = self.pep.receive_message({
			"type": PoliciesTypes.REQUEST_TWEET_REPLY,
			"bot_id": data['bot_id'],
			"bot_id_str": data['bot_id_str'],
			"tweet_id": tweet['id'],
			"tweet_id_str": tweet["id_str"],
			"user_id": tweet['user']['id'],
			"user_id_str": tweet["user"]["id_str"],
			"tweet_text": data['data']['full_text'] if 'full_text' in data['data'] else data['data']['text'],
			"tweet_entities": tweet['entities'],
			"tweet_in_reply_to_status_id_str": tweet['in_reply_to_status_id_str'],
			"tweet_in_reply_to_user_id_str": tweet['in_reply_to_user_id_str'],
			"tweet_in_reply_to_screen_name": tweet['in_reply_to_screen_name']
		})

		if request_accepted:
			log.info(f"Bot {data['bot_id']} request accepted to reply {tweet['id']}")

			self.postgres_client.insert_log({
				"bot_id": int(data["bot_id_str"]),
				"action": log_actions.REPLY_REQ_ACCEPT,
				"target_id": int(tweet['id_str'])
			})

			# also save the thread
			if tweet['in_reply_to_status_id_str']:
				self.postgres_client.insert_log({
					"bot_id": int(data["bot_id_str"]),
					"action": log_actions.REPLY_REQ_ACCEPT,
					"target_id": int(tweet['in_reply_to_status_id_str'])
				})

			# get bot policies
			policy_list = self.postgres_client.search_policies({
				"bot_id": int(data["bot_id_str"]),
				"filter": "Keywords"
			})

			keywords = []
			if policy_list['success']:
				keywords = random.choice(policy_list["data"])["params"]

			# remove urls, tags from text and emojis
			prepared_text = tweet_to_simple_text(tweet['text'] if 'full_text' not in tweet else tweet['full_text'])

			reply_text = self.replier.generate_response(prepared_text, keywords=keywords)
			if reply_text:
				log.info(f"Sending reply text <{reply_text}>")

				self.send(data['bot_id'], ServerToBot.POST_TWEET, {
					"reply_id": tweet['id'],
					"text": reply_text
				})

				self.postgres_client.insert_log({
					"bot_id": data["bot_id_str"],
					"action": log_actions.REPLY_REQ_ACCEPT,
					"target_id": tweet['id_str']
				})
			else:
				log.warning(f"Could not send reply to tweet because of no response from text generator")
		else:
			log.warning(f"Bot {data['bot_id']} request denied to reply {tweet['id']}")
			self.postgres_client.insert_log({
				"bot_id": data["bot_id_str"],
				"action": log_actions.REPLY_REQ_DENY,
				"target_id": tweet['id_str']
			})

	def __request_follow_user(self, data):
		"""
		Action to request a follow:
				Calls the control center to request the follow
				Adds the log to postgres_stats, for the request and its result
				The result is based on the Policy API object

		@param data: dict containing the bot id and the user id
		"""

		user = data['data']['user']
		tweets = data['data']['tweets']
		user_id = user['id']
		user_id_str = user['id_str']
		user_protected = user['protected'] if 'protected' in user else False

		log.info(f"Bot {data['bot_id']} requests a follow from {user_id}")

		# verify if some bot already requested to follow the user
		if self.__found_in_logs(action=log_actions.FOLLOW_REQ_ACCEPT, target=user_id_str, max_number_hours=0):
			log.info(f"Action was already accepted recently for some bot.")
			return

		# verify if the bot already requested to follow user
		if self.__found_in_logs(action=log_actions.FOLLOW_REQ, bot=data["bot_id_str"], target=user_id_str, max_number_hours=0):
			log.info(f"Action was already requested by this bot.")
			return

		self.postgres_client.insert_log({
			"bot_id": int(data["bot_id_str"]),
			"action": log_actions.FOLLOW_REQ,
			"target_id": user_id_str
		})

		request_accepted = self.pep.receive_message({
			"type": PoliciesTypes.REQUEST_FOLLOW_USER,
			"bot_id": data['bot_id'],
			"bot_id_str": data['bot_id_str'],
			"user_id": user_id,
			"user_id_str": user_id_str,
			'user_protected': user_protected
		})

		if request_accepted:
			log.info(f"Following protected user with id str <{user_id_str}>")
			self.__follow_user({
				'data': {
					'status': True,
					'bot_id_str': data['bot_id_str'],
					'user': {
						'id': user_id,
						'id_str': user_id_str
					}
				}
			})
			return

		# get the policies to this bot
		policies = self.postgres_client.search_policies({
			"bot_id": int(data["bot_id_str"])
		})

		activated_notifications = self.postgres_client.search_notifications({"status": True})
		if not activated_notifications['success']:
			activated_notifications = []
		else:
			activated_notifications = activated_notifications['data']

		all_policies = self.postgres_client.search_policies()

		if policies['success'] and all_policies['success']:
			params = {
				'user': user,
				'bot_id_str': data["bot_id_str"],
				'tweets': [t['full_text'] for t in tweets],
				'policies': policies['data'],
				'all_policies': all_policies['data'],
				'activated_notifications': activated_notifications
			}

			self.send_to_follow_user_service(ServerToFollowService.REQUEST_FOLLOW_USER, params)

		for tweet in tweets:
			data['data'] = tweet
			self.save_tweet([data])

	def __follow_user(self, data):
		"""
		Function that sends a follow user  action status (Accepted, denied) to bot
		@param data: dict containing the necessary info
		"""

		status = data['data']['status']
		user = data['data']['user']
		bot_id = int(data['data']['bot_id_str'])
		user_id = user['id']
		user_id_str = user['id_str']

		if status:
			log.info(f"Bot {bot_id} request accepted to follow {user_id}")

			self.postgres_client.insert_log({
				"bot_id": bot_id,
				"action": log_actions.FOLLOW_REQ_ACCEPT,
				"target_id": user_id_str
			})

			self.send(bot_id, ServerToBot.FOLLOW_USERS, {"type": "id", "data": [user_id_str]})
		else:
			log.warning(f"Bot {bot_id} request denied to follow {user_id}")
			self.postgres_client.insert_log({
				"bot_id": bot_id,
				"action": log_actions.FOLLOW_REQ_DENY,
				"target_id": user_id_str
			})

	def __save_dbs(self):
		self.mongo_client.save()
		self.neo4j_client.save_all()
		self.postgres_client.save_all()

	def save_user(self, data_list):
		"""
		Stores info about a list of users:
				Calls the neo4j and the mongo object to update or store the user be it a bot or a user)
				Adds the log of the operation to postgres_stats
				If the user is a bot, must also call the Policy API object

		@param data: dict containing the id of the bot and the user object
		"""

		for data in data_list:
			data_id_in_redis = self.redis_client.get(data['data']['id_str'])
			if data_id_in_redis and data_id_in_redis == mongo_utils.NOT_BLANK:
				log.info("User id found in Redis")
				continue

			log.info(f"Saving User <{data['data']['id']}>")

			user, bot_id, bot_id_str = data["data"], data["bot_id"], data["bot_id_str"]

			exists_in_neo4j = self.neo4j_client.check_bot_exists(bot_id_str)
			if not exists_in_neo4j:
				log.info(f"Bot {bot_id} is new to the party {data}")

				# save bot to mongo and neo4j
				self.neo4j_client.add_bot({
					"id": bot_id_str,
					"name": data['bot_name'],
					"username": data['bot_screen_name']
				})

				# we send the list of initial users to follow
				# follow_list = self.pep.first_time_policy()

				bot_policies = self.postgres_client.search_policies({
					"bot_id": int(data["bot_id_str"])
				})

				bot_policies_args = []
				for policy in bot_policies:
					bot_policies_args += policy['params']

				self.send(bot_id, ServerToBot.FOLLOW_FIRST_TIME_USERS, {
					'queries': bot_policies_args
				})
				"""
				self.send(bot_id, ServerToBot.FOLLOW_USERS, {
					"type": "screen_name",
					"data": follow_list,
				})
				"""
				self.__save_dbs()

			is_bot = self.neo4j_client.check_bot_exists(user["id_str"])
			if is_bot:
				log.info("It's a bot that's already been registered in the database")
				# Update the info of the bot
				exists_in_mongo = self.mongo_client.search(
					collection="users",
					query={"id_str": user['id_str']},
					single=True
				)
				if not exists_in_mongo:
					self.mongo_client.insert_users(user)
				else:
					self.mongo_client.update_users(
						match={"id_str": user['id_str']},
						new_data=user,
						all=False
					)
					self.neo4j_client.update_bot({
						"id": user['id_str'],
						"name": user['name'],
						"username": user['screen_name']
					})
			else:
				if self.neo4j_client.check_user_exists(user["id_str"]) or data_id_in_redis:
					log.info(f"User {user['id']} has already been registered in the database")
					if "is_blank" in user:
						user.pop("is_blank")
					self.mongo_client.update_users(
						match={"id_str": user['id_str']},
						new_data=user,
						all=False
					)
					self.neo4j_client.update_user({
						"id": user["id_str"],
						"name": user['name'],
						"username": user['screen_name'],
						"protected": user['protected']
					})
					self.postgres_client.insert_log({
						"bot_id": bot_id,
						"action": log_actions.UPDATE_USER,
						"target_id": user['id_str']
					})
				else:
					log.info(f"User {user['id']} is new to the party")
					is_blank = "is_blank" in user and user['is_blank']
					self.redis_client.set(user["id_str"], mongo_utils.BLANK if is_blank else mongo_utils.NOT_BLANK)
					if is_blank:
						user.pop("is_blank")

					self.mongo_client.insert_users(user)
					self.neo4j_client.add_user({
						"id": user["id_str"],
						"name": user['name'],
						"username": user['screen_name'],
						"protected": user['protected']
					})
					self.postgres_client.insert_log({
						"bot_id": bot_id,
						"action": log_actions.INSERT_USER,
						"target_id": user['id_str']
					})
					
				self.postgres_client.insert_user({
					"user_id": int(user['id_str']),
					"followers": user["followers_count"],
					"following": user["friends_count"],
					"protected": user["protected"]
				})

				if 'following' in user and user['following']:
					self.__find_followers(bot_id_str, user['id_str'])

	def __save_user_or_blank_user(self, data):
		user = data['data']
		user_id_str = user['id_str']

		user_exists = self.neo4j_client.check_user_exists(user_id_str) \
					  or self.neo4j_client.check_bot_exists(user_id_str)

		if not user_exists or 'name' not in user or not user['name']:
			blank_user = mongo_utils.BLANK_USER.copy()
			blank_user["id"] = user['id']
			blank_user["id_str"] = str(user['id'])
			blank_user["screen_name"] = user['screen_name']

			log.debug(f"Inserting blank user with id {blank_user['id']}")

			log.info("Have to get the full information on the User")
			self.send(
				bot=data["bot_id_str"],
				message_type=ServerToBot.GET_USER_BY_ID,
				params=user['id_str']
			)

			data['data'] = blank_user
			data['data']['is_blank'] = True

		self.save_user([data])
		return self.__user_type(user['id'])

	def __save_blank_tweet_if_dont_exists(self, data):
		tweet_exists = self.mongo_client.search(
			collection="tweets",
			query={"id_str": data["id_str"]},
			single=True
		)

		if tweet_exists:
			return

		log.debug(f"Inserting blank tweet with id {data['id']}")
		blank_tweet = mongo_utils.BLANK_TWEET.copy()
		blank_tweet["id"] = data["id"]
		blank_tweet["id_str"] = data["id_str"]
		blank_tweet["user"] = data["user"]
		blank_tweet["is_blank"] = True

		self.save_tweet([{
			"bot_id": data["bot_id"],
			"bot_id_str": data["bot_id_str"],
			'bot_name': data["bot_name"],
			'bot_screen_name': data["bot_screen_name"],
			"data": blank_tweet
		}])

		log.info("Have to get the full information on the tweet")
		self.send(
			bot=data["bot_id"],
			message_type=ServerToBot.GET_TWEET_BY_ID,
			params=data["id_str"]
		)

	def save_tweet(self, data_list):
		"""
		Stores info about a tweet:
				Calls the mongo object to save or update a tweet
				Saves the tweet on the neo4j object
				Adds the operation log to postgres_stats

		@param data: dict containing the id of the tweet to bee saved
		"""
		log.info(f"Received bulk of tweets {data_list}")
		for data in data_list:
			data_id_in_redis = self.redis_client.get(data['data']['id_str'])
			if data_id_in_redis and data_id_in_redis == mongo_utils.NOT_BLANK:
				log.info("Tweet id found in Redis")
				continue

			log.info(f"Saving Tweet with id=<{data['data']['id_str']}>")

			tweet_exists = self.mongo_client.search(
				collection="tweets",
				query={"id_str": data["data"]["id_str"]},
				single=True
			)

			if data_id_in_redis and tweet_exists:
				log.info(f"Updating tweet {data['data']['id']}")
				self.mongo_client.update_tweets(
					match={"id_str": data["data"]['id_str']},
					new_data=data["data"],
					all=False
				)

				self.postgres_client.insert_log({
					"bot_id": int(data["bot_id_str"]),
					"action": log_actions.UPDATE_TWEET,
					"target_id": int(data['data']['id_str'])
				})
			else:
				is_blank = "is_blank" in data["data"] and data["data"]['is_blank']
				self.redis_client.set(data["data"]["id_str"], mongo_utils.BLANK if is_blank else mongo_utils.NOT_BLANK)
				if is_blank:
					data["data"].pop("is_blank")

				self.postgres_client.insert_log({
					"bot_id": int(data["bot_id_str"]),
					"action": log_actions.INSERT_TWEET,
					"target_id": int(data['data']['id_str'])
				})

				log.info(f"Inserting tweet {data['data']['id']} on Mongo")
				self.mongo_client.insert_tweets(data['data'])

				log.info(f"Inserting tweet {data['data']['id']} on Neo4j")
				self.neo4j_client.add_tweet({
					"id": data['data']['id_str']
				})

				new_data = data.copy()
				new_data["data"] = data["data"]["user"]
				user_type = self.__save_user_or_blank_user(data=new_data)

				self.neo4j_client.add_writer_relationship({
					"user_id": data["data"]["user"]["id_str"],
					"tweet_id": data["data"]["id_str"],
					"user_type": user_type
				})

				if "in_reply_to_status_id" in data["data"] and data["data"]["in_reply_to_status_id"]:
					log.info(f"Tweet was a reply to some other tweet, must insert the reply relation too")
					new_data["id"] = data["data"]["in_reply_to_status_id"]
					new_data["id_str"] = data["data"]["in_reply_to_status_id_str"]
					new_data["user"] = {
						'id': data["data"]["in_reply_to_user_id"],
						'id_str': data["data"]["in_reply_to_user_id_str"],
						'screen_name': data["data"]["in_reply_to_screen_name"]
					}
					self.__save_blank_tweet_if_dont_exists(data=new_data)

					self.neo4j_client.add_reply_relationship({
						"reply": data["data"]["id_str"],
						"tweet": data["data"]["in_reply_to_status_id_str"]
					})

					if user_type == neo4j_labels.BOT_LABEL:
						self.__reply_tweet_log({
							"bot_id": data["data"]["user"]["id_str"],
							"target_id": data["data"]["id_str"]
						})

				elif ("is_quote_status" in data["data"] and data["data"]["is_quote_status"]
					  and "quoted_status" in data["data"]):

					log.info(f"Tweet was quoting some other tweet, must insert the quote relation too")
					new_data["data"] = data["data"]["quoted_status"]
					self.save_tweet([new_data])

					self.neo4j_client.add_quote_relationship({
						"tweet_id": data["data"]["id_str"],
						"quoted_tweet": data["data"]["quoted_status_id_str"]
					})

					if user_type == neo4j_labels.BOT_LABEL:
						self.__quote_tweet_log({
							"bot_id": data["data"]["user"]["id_str"],
							"target_id": data["data"]["id_str"]
						})

				elif "retweeted_status" in data["data"] and data["data"]["retweeted_status"] is not None:
					log.info(f"Tweet was a retweet to some other tweet")
					new_data["data"] = data["data"]["retweeted_status"]

					self.save_tweet([new_data])

					self.neo4j_client.add_retweet_relationship({
						"tweet_id": data["data"]["retweeted_status"]["id_str"],
						"user_id": data["data"]["user"]["id_str"],
						"user_type": user_type
					})

					if user_type == neo4j_labels.BOT_LABEL:
						self.__retweet_log({
							"bot_id": data["data"]["user"]["id_str"],
							"target_id": data["data"]["id_str"]
						})

			log.info(f"Inserting tweet {data['data']['id']} on Postgres")

			self.postgres_client.insert_tweet({
				"tweet_id": int(data['data']['id_str']),
				"user_id": int(data['data']['user']['id_str']),
				"likes": data['data']['favorite_count'],
				"retweets": data['data']['retweet_count']
			})

	def save_dm(self, data):
		"""
		Stores the info about a bot's direct messages:
				Calls the mongo object to save or update a dm
				Adds the operation log to postgres_stats

		@param data: dict containignt the id of the bot and the DMs
		"""
		for message in data['data']:
			message["bot_id"] = data["bot_id"]
			message_exists = self.mongo_client.search(
				collection="messages",
				query={"id_str": message["bot_id_str"]},
				single=True
			)
			if not message_exists:
				log.info(f"New message {data['data']['id']}")
				self.postgres_client.insert_log({
					"bot_id": int(data["bot_id_str"]),
					"action": log_actions.INSERT_MESSAGE,
					"target_id": int(data['data']['id_str'])
				})
				self.mongo_client.insert_messages(message)

	def error(self, data):
		"""
		Stores error that may have occurred in the running of a bot:
				Calls the postgres stats to log the error

		@param data: dict with the id of a bot and the error object
		"""
		self.postgres_client.insert_log({
			"bot_id": data["bot_id"],
			"action": f"ERROR: {data['data']['message']}",
			"target_id": data['data']['target_id']
		})
		log.error(f"Error in trying to do action <{data['data']}>")

	def __add_followers(self, data):
		"""
		Function that writes the follow relationship on the Neo4j API database;
		The function will also request for the bot who sent the message to follow the users who follow
		one of the bot's followers

		@param data: dict with the id of a bot and a second dictionary with the bot's followers' ID as keys that map
		to his followers
		"""
		bot_id = data['bot_id']
		bot_id_str = data['bot_id_str']
		user_id = data['data']['id']
		user_id_str = str(user_id)
		followers = data['data']['followers']

		log.info(f"Starting to create the Follow Relationship for user {user_id}")
		is_bot = self.neo4j_client.check_bot_exists(user_id_str)

		for follower in followers:
			if is_bot:
				self.postgres_client.insert_log({
					"bot_id": bot_id,
					"action": "FOLLOWERS",
					"target_id": follower['id']
				})
				log.info(f"Save list of followers for {follower['id']}")

			# add or update user in databases and its relation with our bot
			self.save_user([{
				'bot_id': bot_id,
				"bot_id_str": bot_id_str,
				'data': follower
			}])

			self.__find_followers(follower['id_str'], user_id_str)

	# TODO -> in the future we can ask the bot to follow this users (when the heuristic to follow someone is done)

	def __send_keywords(self, data):
		log.info("Starting to sending the keywords to the bot")

		bot_id = data["bot_id"]

		policies = self.postgres_client.search_policies({
			"bot_id": bot_id, "filter": "Keywords"
		})

		response = []

		if policies['success']:
			policy_list = policies['data']
			log.debug(f"Obtained policies: {policy_list}")

			if len(policy_list) > 0:
				response = random.choice(policy_list)["params"]

			log.debug(f"Keywords to send: {response}")

			log.info(f"Sending keywords {response} to bot {response}")
		self.send(
			bot_id,
			ServerToBot.KEYWORDS,
			response
		)

	def __user_type(self, user_id: str) -> str:
		if self.neo4j_client.check_bot_exists(user_id):
			return neo4j_labels.BOT_LABEL

		log.warning(f"User with id <{user_id}> is a user")
		return neo4j_labels.USER_LABEL

	def send(self, bot, message_type, params):
		"""
		Function the task uses to send messages through rabbit

		@param bot: id of the bot to reply
		@param message_type: ResponseTypes object with the type of message
		@param params: dict with arguments of the message
		"""
		log.info(f"Sending {message_type.name} to Bot with ID: <{bot}>")
		payload = {
			'type': message_type,
			'params': params
		}
		if self.old_bot != bot:
			if self.old_bot:
				self.__force_send()
			self.old_bot = bot
			self.messages_to_send = []
		self.messages_to_send.append(payload)

	def __force_send(self):
		if len(self.messages_to_send) == 0:
			log.info(f"No messages to send to {self.old_bot}")
			return
		try:
			log.info(f"Sending messages <{self.messages_to_send}>")
			self.rabbit_wrapper.send(queue=TASKS_QUEUE_PREFIX,
									 routing_key=f"{TASKS_ROUTING_KEY_PREFIX}." + str(self.old_bot),
									 message=self.messages_to_send,
									 father_exchange=self.exchange)
		except Exception as error:
			log.exception(f"Failed to send messages <{self.messages_to_send}> because of error <{error}>: ")
			raise error
		self.messages_to_send = []

	def send_to_follow_user_service(self, message_type, params):
		"""
		Function the task uses to send messages through rabbit to follow user service

		@param message_type: ResponseTypes object with the type of message
		@param params: dict with arguments of the message
		"""
		log.info(f"Sending {message_type.name} to follow user service")
		log.debug(f"Content: {params}")
		payload = {
			'type': message_type,
			'params': params
		}
		try:
			self.rabbit_wrapper.send(queue=TASK_FOLLOW_QUEUE, routing_key=TASK_FOLLOW_ROUTING_KEY_PREFIX,
			                         message=payload, father_exchange=self.exchange)
		except Exception as error:
			log.exception(f"Failed to send message <{payload}> because of error <{error}>: ")
			raise error

	def received_message_handler(self, channel, method, properties, body):
		log.info("MESSAGE RECEIVED")
		self.exchange = method.exchange
		self.deliver_tag = method.delivery_tag
		self.channel = channel

		# acknowledge message
		log.info("Acknowledging the consumed message")
		self.channel.basic_ack(self.deliver_tag)
		log.info("Acknowledged the consumed message")

		log.debug(f"Starting to process a new message from exchange <{self.exchange}>")
		message = json.loads(body)
		self.action(message)

	def close(self):
		self.pep.pdp.close()
		self.neo4j_client.close()
