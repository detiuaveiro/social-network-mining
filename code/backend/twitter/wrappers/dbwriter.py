import logging
import sys
from mongo_wrapper import MongoAPI
from neo4j_wrapper import Neo4jAPI
from postgresql_wrapper import PostgresAPI
from enums import *
from rabbitmq import *

sys.path.append("../policies/")
from PEP import PEP

log = logging.getLogger('Database Writer')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
	"[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s"))
log.addHandler(handler)


class DBWriter:
	"""
	Class to smulate the behaviour of a bot:
	On receiving a message from a message broker, this class will act accordingly
	"""

	def __init__(self):
		"""
		This will start instaces for all the DB's API
		"""

		self.postgress_client = PostgresAPI()
		self.mongo_client = MongoAPI()
		self.neo4j_client = Neo4jAPI()
		self.pep = PEP()

	def action(self, message):
		message_type = message['type']

		if message_type == MessageTypes.USER_FOLLOWED:
			self.follow_user(message)

		elif message_type == MessageTypes.TWEET_LIKED:
			self.like_tweet(message)

		elif message_type == MessageTypes.TWEET_RETWEETDED:
			self.retweet(message)

		elif message_type == MessageTypes.TWEET_REPLIED:
			self.reply_tweet(message)

		elif message_type == MessageTypes.REQUEST_TWEET_LIKE:
			self.request_tweet_like(message)

		elif message_type == MessageTypes.REQUEST_TWEET_RETWEET:
			self.request_retweet(message)

		elif message_type == MessageTypes.REQUEST_TWEET_REPLY:
			self.request_tweet_reply(message)

		elif message_type == MessageTypes.REQUEST_FOLLOW_USER:
			self.request_follow_user(message)

		elif message_type == MessageTypes.SAVE_USER:
			self.save_user(message)

		elif message_type == MessageTypes.SAVE_TWEET:
			self.save_tweet(message)

		elif message_type == MessageTypes.SAVE_DIRECT_MESSAGES:
			self.save_dm(message)

		elif message_type == MessageTypes.ERROR_BOT:
			self.error(message)

		elif message_type == MessageTypes.FIND_FOLLOWERS:
			self.find_followers(message)

	# Need DB API now
	def follow_user(self, data):
		"""
		Action to follow user:
				Calls neo4j to add new relation between bot and user
				Calls postgres_stats to add new log with the action details

		@param data: dict containing bot and the user he's following
		"""
		log.info("A bot has started following someone")
		type1 = "Bot" if self.neo4j_client.check_bot_exists(
			data["bot_id"]) else "User"
		type2 = "Bot" if self.neo4j_client.check_bot_exists(
			data["data"]["id"]) else "User"
		relationship = {
			"id_1": data["bot_id"],
			"id_2": data["data"]["id"],
			"type_1": type1,
			"type_2": type2
		}
		if self.neo4j_client.check_relationship_exists(relationship):
			log.info("The bot already follows the user")
			return
		self.neo4j_client.add_relationship(relationship)
		self.postgress_client.insert_log({
			"bot_id": data["bot_id"],
			"action": f"FOLLOW: {data['bot_id']} and {data['data']['id']}"
		})

	def like_tweet(self, data):
		"""
		Action to like tweet:
				Calls postgres_stats to add new log

		@param data dict with the bot id and the tweet he liked
		"""
		self.postgress_client.insert_log({
			"bot_id": data["bot_id"],
			"action": f"TWEET LIKED: {data['bot_id']} and {data['data']['id']}"
		})

	def retweet(self, data):
		"""
		Action to retweet:
				Calls postgres_stats to add new log

		@param data: dict containing bot and the tweet he retweeted
		"""
		self.postgress_client.insert_log({
			"bot_id": data["bot_id"],
			"action": f"RETWEET: {data['bot_id']} and {data['data']['id']}"
		})

	def reply_tweet(self, data):
		"""
		Action to reply a tweet:
				Calls progres_stats to add what the bot replied and to which tweet

		@param data: dict contaning bot and the reply they made
		"""
		self.postgress_client.insert_log({
			"bot_id": data["bot_id"],
			"action": f"TWEET REPLIED: {data['bot_id']} and {data['data']['id']}"
		})

	def request_tweet_like(self, data):
		"""
		Action to request a like on tweeter:
				Calls the PEP to request a like
				Adds the log to postgres_stats, for the request and its result
				The result is based on the PDP methods

		@param data: dict containing the bot id and the tweet id
		"""
		log.info("Request a like to a tweet")
		self.postgress_client.insert_log({
			"bot_id": data["bot_id"],
			"action": f"REQUEST LIKE: {data['bot_id']} and {data['data']['id']} \
			for tweet {data['data']['id']}"
		})
		request_accepted = self.pep.receive_message({
			"type": PoliciesTypes.REQUEST_TWEET_LIKE,
			"bot_id": data['bot_id'],
			"user_id": data['data']['user'],
			"tweet_id": data['data']['id'],
			"tweet_text": data['data']['text'],
			"tweet_entities": data['data']['entities']
		})

		if True:
			log.info("Like request accepted")
			self.postgress_client.insert_log({
				"bot_id": data["bot_id"],
				"action": f"REQUEST LIKE ACCEPTED: {data['bot_id']} and {data['data']['id']} \
				for tweet {data['data']['id']}"
			})
			self.send(
				data['bot_id'], ResponseTypes.LIKE_TWEETS,
				data['data']['id']
			)
		else:
			log.warning("Like request denied")
			self.postgress_client.insert_log({
				"bot_id": data["bot_id"],
				"action": f"REQUEST LIKE DENIED: {data['bot_id']} and {data['data']['id']} \
				for tweet {data['data']['id']}"
			})

	def request_retweet(self, data):
		"""
		Action to request a retweet:
				Calls the PEP to request the retweet
				Adds the log to postgres_stats, for the request and its result
				The result is based on the PDP methods

		2param data: dict containing the bot id and the tweet id
		"""
		log.info("Request a retweeting a tweet")
		self.postgress_client.insert_log({
			"bot_id": data["bot_id"],
			"action": f"RETWEET REQUEST: {data['bot_id']} and {data['data']['user']} \
			for tweet {data['data']['id']}"
		})
		request_accepted = self.pep.receive_message({
			"type": PoliciesTypes.REQUEST_TWEET_RETWEET,
			"bot_id": data['bot_id'],
			"user_id": data['data']['user'],
			"tweet_id": data['data']['id'],
			"tweet_text": data['data']['text'],
			"tweet_entities": data['data']['entities']
		})

		if request_accepted:
			log.info("Retweet request accepted")
			self.postgress_client.insert_log({
				"bot_id": data["bot_id"],
				"action": f"RETWEET REQUEST ACCEPTED: {data['bot_id']} and {data['data']['user']} \
				for tweet {data['data']['id']}"
			})
			self.send(
				data['bot_id'],
				ResponseTypes.RETWEET_TWEETS, data['data']['id']
			)
		else:
			log.warning("Retweet request denied")
			self.postgress_client.insert_log({
				"bot_id": data["bot_id"],
				"action": f"RETWEET REQUEST DENIED: {data['bot_id']} and {data['data']['user']} \
				for tweet {data['data']['id']}"
			})

	def request_tweet_reply(self, data):
		"""
		Action to request a reply:
				Calls the control center to request the reply
				Adds the log to postgres_stats, for the request and its result
				The result is based on the Policy API object

		@param data: dict containing the bot id and the tweet id
		"""
		log.info("Request a reply to a tweet")
		self.postgress_client.insert_log({
			"bot_id": data["bot_id"],
			"action": f"REPLY REQUEST: {data['bot_id']} and {data['data']['id']} \
			for tweet {data['data']['id']}"
		})
		request_accepted = self.pep.receive_message({
			"type": PoliciesTypes.REQUEST_TWEET_REPLY,
			"bot_id": data['bot_id'],
			"tweet_id": data['data']['id'],
			"user_id": data['data']['user'],
			"tweet_text": data['data']['text'],
			"tweet_entities": data['data']['entities'],
			"tweet_in_reply_to_status_id_str": data['data']['in_reply_to_status_id_str'],
			"tweet_in_reply_to_user_id_str": data['data']['in_reply_to_user_id_str'],
			"tweet_in_reply_to_screen_name": data['data']['in_reply_to_screen_name']
		})

		if request_accepted:
			log.info("Like request accepted")
			self.postgress_client.insert_log({
				"bot_id": data["bot_id"],
				"action": f"REPLY REQUEST ACCEPTED: {data['bot_id']} and {data['data']['id']} \
				for tweet {data['data']['id']}"
			})
			self.send(
				data['bot_id'], ResponseTypes.POST_TWEETS,
				data['data']['id'])
		else:
			log.warning("Like request denied")
			self.postgress_client.insert_log({
				"bot_id": data["bot_id"],
				"action": f"REPLY REQUEST DENIED: {data['bot_id']} and {data['data']['id']} \
				for tweet {data['data']['id']}"
			})

	def request_follow_user(self, data):
		"""
		Action to request a follow:
				Calls the control center to request the follow
				Adds the log to postgres_stats, for the request and its result
				The result is based on the Policy API object

		@param data: dict containing the bot id and the tweet id
		"""
		log.info("Request a like to a tweet")
		self.postgress_client.insert_log({
			"bot_id": data["bot_id"],
			"action": f"FOLLOW REQUEST: {data['bot_id']} and {data['data']['id']}"
		})
		request_accepted = self.pep.receive_message({
			"type": PoliciesTypes.REQUEST_FOLLOW_USER,
			"bot_id": data['bot_id'],
			"user_id": data['data']['id']
		})

		if request_accepted:
			log.info("Like request accepted")
			self.postgress_client.insert_log({
				"bot_id": data["bot_id"],
				"action": f"FOLLOW REQUEST ACCEPTED: {data['bot_id']} and {data['data']['id']}"
			})
			self.send(
				data['bot_id'], ResponseTypes.FOLLOW_USERS,
				data['data']['id'])
		else:
			log.warning("Like request denied")
			self.postgress_client.insert_log({
				"bot_id": data["bot_id"],
				"action": f"FOLLOW REQUEST DENIED: {data['bot_id']} and {data['data']['id']}"
			})

	def save_user(self, data):
		"""
		Stores info about a user:
				Calls the neo4j and the mongo object to update or store the user be it a bot or a user)
				Adds the log of the operation to postgress_stats
				If the user is a bot, must also call the Policy API object

		@param data: dict containing the id of the bot and the user object
		"""
		log.info("Saving User")
		log.info(
			"First we check if the bot sending the message has been in the database")
		exists = self.neo4j_client.check_bot_exists(data["bot_id"])
		if not exists:
			log.info("Bot is new to the party")
			follow_list = self.pep.first_time_policy()
			self.send(data["bot_id"], ResponseTypes.FOLLOW_USERS, {
				"type": "screen_name", "data": follow_list})
			self.mongo_client.insert_users(data["data"])
			self.neo4j_client.add_bot(
				{"id": data["data"]['id'], "name": data['data']['name'], "username": data['data']['screen_name']})
		else:

			is_bot = self.neo4j_client.check_bot_exists(data["data"]["id"])
			if is_bot:
				log.info(
					"It's a bot that's already been registered in the database")
				# Update the info of the bot
				self.mongo_client.update_users(
					match={"id": data["data"]['id']},
					new_data=data["data"],
					all=False
				)
				self.neo4j_client.update_bot(
					{"id": data["data"]['id'], "name": data['data']['name'], "username": data['data']['screen_name']})

			else:
				if self.neo4j_client.check_user_exists(data["data"]["id"]):
					log.info(
						"It's a user that's already been registered in the database")
					self.mongo_client.update_users(
						match={"id": data["data"]['id']},
						new_data=data["data"],
						all=False
					)
					self.neo4j_client.update_user({
						"id": data["data"]["id"],
						"name": data['data']['name'],
						"username": data['data']['screen_name']
					})
					self.postgress_client.insert_log({
						"bot_id": data["bot_id"],
						"action": f"Updating info for {data['data']['id']}"
					})

				else:
					log.info("User is new to the party")
					self.mongo_client.insert_users(data["data"])
					self.neo4j_client.add_user({
						"id": data["data"]["id"],
						"name": data['data']['name'],
						"username": data['data']['screen_name']
					})
					self.postgress_client.insert_log({
						"bot_id": data["bot_id"],
						"action": f"Inserting info for {data['data']['user']}"
					})
				self.postgress_client.insert_user({
					"user_id": data["data"]["id"],
					"followers": data["data"]["followers_count"],
					"following": data["data"]["friends_count"]
				})

	def save_tweet(self, data):
		"""
		Stores info about a tweet:
				Calls the mongo object to save or update a tweet
				Adds the operation log to postgress_stats

		@param data: dict containing the id of the tweet to bee saved
		"""
		tweet_exists = self.mongo_client.search(
			collection="tweets",
			query={"id": data["data"]["id"]},
			single=True
		)
		if tweet_exists:
			log.info("Updating tweet")
			self.mongo_client.update_tweets(
				match={"id": data["data"]['id']},
				new_data=data["data"],
				all=False
			)
			self.postgress_client.insert_log({
				"bot_id": data["bot_id"],
				"action": f"Updating tweet for {data['data']['id']}"
			})
		else:
			log.info("Inserting tweet")
			self.mongo_client.insert_tweets(data['data'])
			self.postgress_client.insert_log({
				"bot_id": data["bot_id"],
				"action": f"Inserting tweet for {data['data']['id']}"
			})
		self.postgress_client.insert_tweet({
			"tweet_id": data['data']['id'],
			"user_id": data['data']['user'],
			"likes": data['data']['favorite_count'],
			"retweets": data['data']['retweet_count']
		})

	def save_dm(self, data):
		"""
		Stores the info about a bot's direct messages:
				Calls the mongo object to save or update a dm
				Adds the operation log to postgress_stats

		@param data: dict containignt the id of the bot and the DMs
		"""
		for message in data['data']:
			message["bot_id"] = data["bot_id"]
			message_exists = self.mongo_client.search(
				collection="messages",
				query={"id": message["bot_id"]},
				single=True
			)
			if not message_exists:
				log.info("NEW MESSAGE")
				self.postgress_client.insert_log({
					"bot_id": data["bot_id"],
					"action": f"Inserting new message {message}"
				})
				self.mongo_client.insert_messages(message)

	def error(self, data):
		"""
		Stores error that may have occured in the running of a bot:
				Calls the postgres stats to log the error

		@param data: dict with the id of a bot and the error object
		"""
		self.postgress_client.insert_log({
			"bot_id": data["bot_id"],
			"action": f"Error occured for {data['data']}"
		})

	def find_followers(self, data):
		"""
		Function that writes the follow relationship on the Neo4j API database;
		The function will also request for the bot who sent the message to follow the users who follow
		one of the bot's followers

		@param data: dict with the id of a bot and a second dictionary with the bot's followers' ID as keys that map
		to his followers
		"""
		log.info("Starting to create the Follow Relationship")
		for follower in data["data"]:
			self.postgress_client.insert_log({
				"id_bot": data['bot_id'],
				"action": f"Save list of followers for {follower}"
			})
			# Verify if the follower is on the database as a user
			is_user = self.neo4j_client.check_user_exists(follower)
			is_bot = self.neo4j_client.check_bot_exists(follower)
			if not (is_user or is_bot):
				# The follower isn't registered in the database, so that must be handled
				self.save_user({
					"bot_id": data["bot_id"],
					"data": {
						"id": int(follower),
						"name": "",
						"screen_name": "",
						"followers_count": 0,
						"friends_count": 0
					}
				})

			for follower_follower in data["data"][follower]:
				follower_follower_is_user = self.neo4j_client.check_user_exists(
					follower_follower)
				if follower_follower_is_user:
					self.request_follow_user({
						"bot_id": data['bot_id'],
						"data": {"id": follower_follower}
					})

				self.follow_user({
					"bot_id": int(follower),
					"data": {
						"id": follower_follower
					}
				})

	def send(self, bot, message_type, params):
		"""
		Function the task uses to send messages through rabbit

		@param bot: id of the bot to reply
		@param message_type: ResponseTypes object with the type of message
		@param params: dict with arguments of the message
		"""
		log.info(f"Sending {message_type.name} to Bot with ID: <{bot}>")
		log.debug(f"Content: {params}")
		payload = {
			"type": message_type,
			"params": params
		}
		try:
			conn = Rabbitmq()
			conn.send(routing_key='tasks.twitter.' + str(bot), message=payload)
			conn.close()
		except Exception as e:
			log.error("FAILED TO SEND MESSAGE:")
			log.error("Error: " + str(e))


	def close(self):
		self.neo4j_client.close()
		self.pep.pdp.close()


if __name__ == "__main__":

	dbwriter = DBWriter()

	tweet = {
		"id": 8912323,
		"text": "RT @nbastats: HISTORY!\n\nSteph Curry and Draymond Green become the first teammates in @NBAHistory \
		to both record a triple-double in the same…",
		"truncated": False,
		"entities": {
			"hashtags": [],
			"symbols": [],
			"user_mentions": [	],
			"urls": []
		},
		"source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
		"in_reply_to_status_id": None,
		"in_reply_to_user_id": None,
		"in_reply_to_screen_name": None,
		"user": 874358,
		"is_quote_status": False,
		"retweet_count": 564,
		"favorite_count": 0,
		"lang": "en"
	}

	dbwriter.save_tweet({
		"bot_id": 874358,
		"data": tweet
	})

	dbwriter.request_tweet_like({
		"bot_id": 874358,
		"data": tweet
	})

	dbwriter.request_follow_user({
		"bot_id": 874358,
		"data": {
			"id": 318689
		}
	})

	dbwriter.save_dm({
		"bot_id": 318689,
		"data": [{
			"id": 12345432123,
			"text": "ola, my first tweet",
			"user": 123234
		}]
	})

	dbwriter.follow_user({
		"bot_id": 318689,
		"data": {
			"id": 123234
		}
	})
	dbwriter.save_user({
		"bot_id": 874358,
		"data": {
			"id": 874358,
			"name": "abc xyz",
			"screen_name": "ina",
			"location": "ygo",
			"description": "fusion monster",
			"followers_count": 0,
			"friends_count": 0
		}
	})

	dbwriter.save_user({
		"bot_id": 318689,
		"data": {
			"id": 318689,
			"name": "abc",
			"screen_name": "buster dragon",
			"location": "ygo",
			"description": "fusion monster",
			"followers_count": 0,
			"friends_count": 0
		}
	})
	dbwriter.save_user({
		"bot_id": 31868,
		"data": {
			"id": 31868,
			"name": "abc",
			"screen_name": "buster dragon",
			"location": "ygo",
			"description": "fusion monster",
			"followers_count": 0,
			"friends_count": 0
		}
	})
	dbwriter.save_user({
		"bot_id": 318689,
		"data": {
			"id": 123234,
			"name": "xyz",
			"screen_name": "the other one",
			"location": "ygo",
			"description": "fusion monster",
			"followers_count": 0,
			"friends_count": 0
		}
	})

	dbwriter.follow_user({
		"bot_id": 318689,
		"data": {
			"id": 123234
		}
	})

	dbwriter.follow_user({
		"bot_id": 875358,
		"data": {
			"id": 123234
		}
	})

	dbwriter.find_followers({
		"bot_id": 318689,
		"data": {
			"123234": [875358]
		}
	})

	dbwriter.close()
