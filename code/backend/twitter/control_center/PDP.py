## @package twitter.control_center
# coding: UTF-8
import random
import datetime
import json
import logging

from control_center.utils import tweet_to_simple_text
from wrappers.mongo_wrapper import MongoAPI
from wrappers.neo4j_wrapper import Neo4jAPI
from wrappers.postgresql_wrapper import PostgresAPI
from control_center.policies_types import PoliciesTypes
import log_actions
from datetime import timedelta, datetime


# Constants used below for the Heuristics
THRESHOLD_LIKE = 0.4
THRESHOLD_RETWEET = 0.6
THRESHOLD_REPLY = 0.6
THRESHOLD_FOLLOW_USER = 0.80
MEAN_WORDS_PER_TWEET = 80
POLICY_KEYWORDS_MATCHES = 0.2
POLICY_USER_IS_TARGETED = 0.4
PENALTY_LIKED_RECENTLY_SMALL = -0.35
PENALTY_LIKED_RECENTLY_SMALL_INTERVAL = 10
PENALTY_LIKED_RECENTLY_LARGE = -0.65
PENALTY_LIKED_RECENTLY_LARGE_INTERVAL = 5
PENALTY_RETWEETED_USER_RECENTLY = -0.5
PENALTY_RETWEETED_USER_RECENTLY_INTERVAL = 43200  # 12 hours
PENALTY_REPLIED_USER_RECENTLY_INTERVAL = 24 * 60 * 60  # a day
PENALTY_REPLIED_USER_RECENTLY = -0.5
BOT_FOLLOWS_USER = 0.3
BOT_RETWEETED_TWEET = 0.2
BOT_LIKED_TWEET = 0.3
REPLY_TWEET_MIN_SIZE = 60  # min length of tweet

NUMBER_TWEETS_FOLLOW_DECISION = 5

LIMIT_LOGS = 200
LIMIT_LOGS_FOLLOW_USERS_PROTECTED = 50

log = logging.getLogger('PDP')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(open("pdp.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)

log = logging.getLogger('PDP')
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("pdp.log", "w"))
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)


class PDP:
	def __init__(self):
		"""
		Here starts the connections with the other DB wrappers
		"""
		self.mongo = MongoAPI()
		self.neo4j = Neo4jAPI()
		self.postgres = PostgresAPI()

	def receive_request(self, data):
		# Leaving this as a simple function call, leaving the room for handling the data available
		return self.evaluate(data)

	def evaluate(self, msg):
		"""
		Workflow of this function:
			1. pre-processing of request (filter, prepare db request, etc)
			2. request to DB
			3. get request from DB
			4. post-processing of response (clean response from db, etc)
			5. DECIDE (PERMIT, DENY)

		@param msg : dict
			Dictionary with necessary fields to perform the query.
			Something of this form: { "type" : action, data }

		@return response:
			A response with either "DENY" or "PERMIT"
		"""

		evaluate_answer = False
		# PRE-PROCESSING the request to get the QUERY
		'''
		prepare the query according to the request
		for all REQUEST_TWEET*, it's based on a heuristic (if it's in the threshold, request accepted): 0 to 1
		if it's a REQUEST_FOLLOW_USER, check the rules to see if it is accepted
		if it's a first time user, give some usernames
		'''
		msg_type = msg["type"]

		if msg_type == PoliciesTypes.REQUEST_TWEET_LIKE:
			'''
			bot_id
			user_id
			tweet_id
			tweet_text
			tweet_entities
				- from entities, fetch hashtags and mentions
			'''
			res = self.analyze_tweet_like(msg)
			evaluate_answer = res > THRESHOLD_LIKE
		elif msg_type == PoliciesTypes.REQUEST_TWEET_RETWEET:
			'''
			bot_id
			user_id
			tweet_id
			tweet_text
			tweet_entities
				- from entities, fetch hashtags and mentions
			'''
			res = self.analyze_tweet_retweet(msg)
			evaluate_answer = res > THRESHOLD_RETWEET
		elif msg_type == PoliciesTypes.REQUEST_TWEET_REPLY:
			'''
			bot_id 
			user_id	
			tweet_id
			tweet_text
			tweet_entities
			tweet_in_reply_to_status_id_str
			tweet_in_reply_to_user_id_str
			tweet_in_reply_to_screen_name
			'''
			evaluate_answer = self.analyze_tweet_reply(msg) > THRESHOLD_REPLY
		elif msg_type == PoliciesTypes.REQUEST_FOLLOW_USER:
			evaluate_answer = self.analyze_follow_user(msg) > THRESHOLD_FOLLOW_USER
		if evaluate_answer:
			log.info(f"Request to {msg_type.name} accepted")
			return self.send_response({"response": "PERMIT"})
		else:
			log.warning(f"Request to {msg_type.name} denied")
			return self.send_response({"response": "DENY"})

	@staticmethod
	def send_response(msg):
		message = json.dumps(msg)
		return message

	@staticmethod
	def get_first_time_list():
		"""
		When a bot connects for the first time to Twitter, he'll have to start following people This is the old way:
		having a set list of possible users and the bot will follow a random group from those followers In future
		iterations we may alter this so that there are possible branches a bot could start with: politics,
		football fan, etc., each branch with a list of possible users to follow

		@return: List of users the bot will start following
		"""
		log.info(f"Creating users for the bot to start following")
		num_users = 6  # random.randint(2, 10)
		with open("control_center/first_time_users.json", "r") as f:
			users = json.load(f)

		bot_list = []
		while len(bot_list) < num_users:
			index = random.randint(0, len(users) - 1)
			bot_list.append(users.pop(index))

		log.info("Sending first time list: " + ", ".join(bot_list))

		return bot_list

	@staticmethod
	def _bot_is_targeted(policy, data):
		"""
		Private function to check if a bot is being targeted in a policy
		Checks first if the bot was mentioned in the tweet, or if the user who posted the tweet is himself listed
		in the policy

		@param policy dictionary containing its information
		@param data dictionary containing important information

		@returns True or False depending if the bot was indeed targeted
		"""
		for mention in data["tweet_entities"]["user_mentions"]:
			if int(mention["id_str"]) in policy["bots"]:
				log.info(f"Bot <{data['bot_id']}> was mentioned by user")
				return True

		if data["user_id"] in policy["bots"]:
			log.info(f"Bot <{data['bot_id']}> was targeted in the policy")

		log.info(f"Bot <{data['bot_id']}> was not targeted in the policy")
		return False

	@staticmethod
	def _tweet_has_keywords(policy, data):
		"""
		Private function to check if a tweet uses any important keywords, be it hashtags or commonly found words

		@param policy dictionary containing its information
		@param data dictionary containing important information

		@returns True or False depending if the tweet has keywords
		"""
		for hashtag in data["tweet_entities"]["hashtags"]:
			if hashtag["text"] in policy["params"]:
				return True

		for keyword in policy["params"]:
			if keyword in data["tweet_text"]:
				return True

		log.info(f"Tweet <{data['tweet_id']}> has no keywords")
		return False

	def _score_for_relation(self, data):
		"""
		Algorithm to attribute a score if there's a follow relationship between the user and the bot

		@param: data - dictionary containing the data of the bot and the tweet to be analyzed
		@returns: float corresponding for the constant attributed to the situation
		"""

		type1 = "Bot" if self.neo4j.check_bot_exists(data["bot_id_str"]) else "User"
		type2 = "Bot" if self.neo4j.check_bot_exists(data["user_id_str"]) else "User"
		relation_exists = self.neo4j.check_follow_exists({
			"id_1": data["bot_id_str"],
			"type_1": type1,
			"id_2": data["user_id_str"],
			"type_2": type2
		})
		if relation_exists:
			log.info(f"Relation exists between {data['bot_id']} and {data['user_id']}")
			return BOT_FOLLOWS_USER
		log.info(f"Relation doesn't exist between {data['bot_id']} and {data['user_id']}")
		return 0

	def _score_for_policies(self, data):
		"""
		Algorithm to atribute a score for the relation the bot and the user have with the policies
		If the bot is being targeted by some policy, or if the tweet has a special keyword, it will return the
		appropriate score

		@param: data - dictionary containing the data of the bot and the tweet to be analyzed
		@returns: float corresponding for the constant attributed to the situation
		"""
		policy_list = self.postgres.search_policies({
			"bot_id": data["bot_id"]
		})

		log.debug(policy_list)

		if policy_list['success']:
			for policy in policy_list["data"]:

				if policy["filter"] == "Target":
					# Check if our bot is being targeted

					if self._bot_is_targeted(policy, data):
						log.debug(f"Bot <{data['bot_id']}> has been targeted by a policy")
						return POLICY_USER_IS_TARGETED

				elif policy["filter"] == "Keywords":
					# Check if tweet has any important keywords (be it a hashtag or a commonly found word)

					if self._tweet_has_keywords(policy, data):
						log.debug(f"Tweet <{data['tweet_id']}> has been keywords")
						return POLICY_KEYWORDS_MATCHES

		return 0

	def analyze_tweet_like(self, data):
		"""
		Algorithm to analyse if a bot should like a Tweet
		Takes the current statistics and turns them into a real value

		@param: data - dictionary containing the data of the bot and the tweet it wants to like
		@returns: float that will then be compared to the threshold previously defined
		"""

		log.info(f"Analyzing possibility to like tweet with id: <{data['tweet_id']}>")

		heuristic_value = 0

		# Verify if there's a relation between the bot and the user
		heuristic_value += self._score_for_relation(data)

		# Next we check if the bot and the user have some policies in common
		heuristic_value += self._score_for_policies(data)

		# We then check if the bot has retweeted the tweet
		bot_logs = self.postgres.search_logs({
			"bot_id": data["bot_id"],
			"action": log_actions.RETWEET,
			"target_id": data["tweet_id"]
		}, limit=1)

		if bot_logs['success'] and len(bot_logs["data"]):
			log.info("Bot has already retweeted the tweet")
			heuristic_value = heuristic_value + BOT_RETWEETED_TWEET if heuristic_value < 0.8 else 1

		# We now check if the last recorded like from a tweet of this user was too recent
		bot_logs = self.postgres.search_logs({
			"bot_id": data["bot_id"],
			"action": log_actions.TWEET_LIKE,
			"timestamp": datetime.now() - timedelta(seconds=PENALTY_LIKED_RECENTLY_LARGE_INTERVAL)
		}, limit=LIMIT_LOGS)
		if bot_logs['success']:
			bot_logs_dict = {}
			for bot_log in bot_logs['data']:
				bot_logs_dict[str(bot_log['target_id'])] = {'timestamp': bot_log["timestamp"]}

			if len(bot_logs_dict) > 0:
				users_of_tweets_liked = self.mongo.search(
					collection="tweets",
					query={"$or": [{"id_str": target_id} for target_id in bot_logs_dict.keys()]},
					fields=["user"],
					single=False
				)

				if users_of_tweets_liked:
					for user_of_tweet_liked in users_of_tweets_liked:
						id_str = user_of_tweet_liked['user']['id_str']
						if id_str == str(data["user_id"]) and id_str in bot_logs_dict:
							log.info(f"Found a past like to the user with id <{data['user_id']}>: {user_of_tweet_liked}")
							date = bot_logs_dict[id_str]['timestamp']
							now = datetime.datetime.now()
							if (now - date).seconds < PENALTY_LIKED_RECENTLY_SMALL_INTERVAL:
								log.info("Bot has liked a tweet from the same user, but may not be that suspicious")
								heuristic_value += PENALTY_LIKED_RECENTLY_SMALL
							else:
								log.info("Bot has recently liked a tweet from the same user")
								heuristic_value += PENALTY_LIKED_RECENTLY_LARGE

		log.info(f"Request to like to tweet <{data['tweet_id']}> with heuristic value of <{heuristic_value}>")
		return heuristic_value

	def analyze_tweet_retweet(self, data):
		"""
		Algorithm to analyse if a bot should retweet a Tweet
		Takes the current statistics and turns them into a real value

		@param: data - dictionary containing the data of the bot and the tweet it wants to like
		@returns: float that will then be compared to the threshold previously defined
		"""

		log.info(f"Analyzing possibility to like retweet with id: <{data['tweet_id']}>")

		heuristic_value = 0
		# Verify if there's a relation between the bot and the user
		heuristic_value += self._score_for_relation(data)

		# Next we check if the bot and the user have some policies in common
		heuristic_value += self._score_for_policies(data)

		# We then check if the bot has liked the tweet
		bot_logs = self.postgres.search_logs({
			"bot_id": data["bot_id"],
			"action": log_actions.TWEET_LIKE,
			"target_id": data["tweet_id"]
		}, limit=1)
		if bot_logs["success"] and len(bot_logs["data"]) > 0:
			log.info("Bot already liked the tweet")
			heuristic_value = heuristic_value + BOT_LIKED_TWEET if heuristic_value < 0.7 else 1

		# Finally check if the bot already retweeted something from the user too recently
		bot_logs = self.postgres.search_logs({
			"bot_id": data["bot_id"],
			"action": log_actions.RETWEET,
			"timestamp": datetime.now() - timedelta(seconds=PENALTY_RETWEETED_USER_RECENTLY_INTERVAL)
		}, limit=LIMIT_LOGS)
		if bot_logs['success']:
			bot_logs_dict = {}
			for bot_log in bot_logs['data']:
				bot_logs_dict[str(bot_log['target_id'])] = {'timestamp': bot_log["timestamp"]}

			if len(bot_logs_dict) > 0:
				users_of_retweets = self.mongo.search(
					collection="tweets",
					query={"$or": [{"id_str": target_id} for target_id in bot_logs_dict.keys()]},
					fields=["user"],
					single=False
				)

				if users_of_retweets:
					for user_of_retweet in users_of_retweets:
						id_str = user_of_retweet['user']['id_str']
						if id_str == str(data["user_id"]) and id_str in bot_logs_dict:
							log.info(f"Found a past retweet to the user with id <{data['user_id']}>: {user_of_retweet}")
							log.debug("Bot has recently retweet the user")
							heuristic_value += PENALTY_RETWEETED_USER_RECENTLY

		log.info(f"Request to retweet to tweet <{data['tweet_id']}> with heuristic value of <{heuristic_value}>")
		return heuristic_value

	def analyze_tweet_reply(self, data):
		"""
		Algorithm to analyse if a bot should reply
		Takes the current statistics and turns them into a real value

		@param: data - dictionary containing the data of the bot and the tweet it wants to like
		@returns: float that will then be compared to the threshold previously defined
		"""

		log.info(f"Analyzing possibility to reply tweet with id: <{data['tweet_id']}>")

		# first, ew verify the length of the tweet
		len_tweet = len(tweet_to_simple_text(data["tweet_text"]))
		if len_tweet < REPLY_TWEET_MIN_SIZE:
			log.info(f"Request to reply to tweet <{data['tweet_id']}> denied because the tweet text has lentgh of "
					 f"{len_tweet}")
			return 0

		# second, we verify if the bot already replied to the tweet
		bot_logs = self.postgres.search_logs({
			"bot_id": data["bot_id"],
			"action": log_actions.REPLY_REQ_ACCEPT,
			"target_id": data["tweet_id"]
		}, limit=LIMIT_LOGS)
		if not bot_logs["success"] or bot_logs['data']:
			log.info(
				f"Request to reply to tweet <{data['tweet_id']}> denied because the bot already replied to this tweet")
			return 0

		heuristic_value = 0
		# Verify if there's a relation between the bot and the user
		heuristic_value += self._score_for_relation(data)

		# Next we check if the bot and the user have some policies in common
		heuristic_value += self._score_for_policies(data)

		# We then check if the bot has liked the tweet
		bot_logs = self.postgres.search_logs({
			"bot_id": data["bot_id"],
			"action": log_actions.RETWEET_REQ_ACCEPT,
			"target_id": data["tweet_id"]
		}, limit=1)
		if bot_logs["success"]:
			log.info(f"Bot already liked the tweet <{data['tweet_id']}>")
			heuristic_value = heuristic_value + BOT_LIKED_TWEET if heuristic_value < 0.7 else 1

		# Finally check if the bot already replied to the user recently
		bot_logs = self.postgres.search_logs({
			"bot_id": data["bot_id"],
			"action": log_actions.TWEET_REPLY,
			"timestamp": datetime.now() - timedelta(seconds=PENALTY_REPLIED_USER_RECENTLY_INTERVAL)
		}, limit=LIMIT_LOGS)

		if bot_logs['success']:
			bot_logs_dict = {}
			for bot_log in bot_logs['data']:
				bot_logs_dict[str(bot_log['target_id'])] = {'timestamp': bot_log["timestamp"]}

			if len(bot_logs_dict) > 0:
				users_of_replies = self.mongo.search(
					collection="tweets",
					query={"$or": [{"id_str": target_id} for target_id in bot_logs_dict.keys()]},
					fields=["user"],
					single=False
				)

				if users_of_replies:
					for user_of_reply in users_of_replies:
						id_str = user_of_reply['user']['id_str']
						if id_str == str(data['user_id']) and id_str in bot_logs_dict:
							log.info(f"Found a past reply to the user with id <{data['user_id']}>: {user_of_reply}")
							date = bot_logs_dict[id_str]['timestamp']
							now = datetime.datetime.now()
							if (now - date).seconds < PENALTY_REPLIED_USER_RECENTLY_INTERVAL:
								log.debug("Bot recently replied to another tweet from user")
								heuristic_value += PENALTY_REPLIED_USER_RECENTLY
								break

		log.info(f"Request to reply to tweet <{data['tweet_id']}> with heuristic value of <{heuristic_value}>")
		return heuristic_value

	def analyze_follow_user(self, data):
		"""Used to follow if the bot already follow some predefined number of people and the requested follow is a
			protected user
		:param data:
		:return:
		"""

		# first, we verify if the user is protected
		if 'user_protected' not in data or not data['user_protected']:
			return 0

		# second, we verify if the bot already follows a large number of users
		bot_logs = self.postgres.search_logs({
			"bot_id": data["bot_id"],
			"action": log_actions.FOLLOW,
			"target_id": data["user_id_str"]
		}, limit=LIMIT_LOGS_FOLLOW_USERS_PROTECTED)

		if bot_logs['success']:
			number_follows = len(bot_logs['data'])
			log.debug(f"The bot follows {number_follows}")

			return 1 if number_follows >= LIMIT_LOGS_FOLLOW_USERS_PROTECTED - 1 else 0
		return 0

	def close(self):
		self.neo4j.close()
