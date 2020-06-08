## @package twitter.wrappers
# coding: UTF-8

import logging
from neo4j import GraphDatabase
import credentials
from neo4j_labels import BOT_LABEL, USER_LABEL, TWEET_LABEL, WROTE_LABEL, \
	RETWEET_LABEL, REPLY_LABEL, FOLLOW_LABEL, QUOTE_LABEL, QUERY
import json

log = logging.getLogger("Neo4j")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("neo4j.log", "w"))
handler.setFormatter(
	logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)


class Neo4jAPI:
	def __init__(self, FULL_URL=credentials.NEO4J_FULL_URL):
		log.debug("Connecting to Neo4j")
		self.driver = GraphDatabase.driver(
			"bolt://" + FULL_URL,
			auth=(credentials.NEO4J_USERNAME, credentials.NEO4J_PASSWORD), encrypted=False
		)

	def close(self):
		self.driver.close()

	def add_bot(self, data):
		"""Method used to create a new bot

		@param data: The params of the new bot we want to create. Should include an id, name and username
		"""
		if (
				"id" not in data.keys()
				or "name" not in data.keys()
				or "username" not in data.keys()
		):
			log.error("ERROR CREATING A BOT")
			log.error(
				"Error: Specified data doesn't contain necessary fields - id, name, username"
			)

			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__create_bot, data)

	def __create_bot(self, tx, data):
		log.debug("CREATING BOT")

		try:
			# Note we use Merge rather than Create to avoid duplicates
			tx.run(f"MERGE (:{BOT_LABEL} {{ name: $name, id: $id, username: $username }} )",
					id=str(data["id"]),
					name=data["name"],
					username=data["username"])
		except Exception as e:
			log.exception(f"Error trying to create a bot -> {e}")

	def add_user(self, data):
		"""Method used to create a new user

		@param data: The params of the new bot we want to create. Should include an id, name and username
		"""
		if (
				"id" not in data.keys()
				or "name" not in data.keys()
				or "username" not in data.keys()
				or "protected" not in data.keys()
		):
			log.error("ERROR CREATING A USER")
			log.debug(
				"Error: Specified data doesn't contain necessary fields - id, name, username, protected"
			)

			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__create_user, data)

	def __create_user(self, tx, data):
		log.debug("CREATING USER")

		try:
			tx.run(f"MERGE (:{USER_LABEL} {{ name: $name, id: $id, username: $username, protected=$protected }})",
					id=str(data["id"]),
					name=data["name"],
					username=data["username"],
				    protected=data["protected"])
		except Exception as e:
			log.exception(f"Error trying to create a User {e}")

	def add_tweet(self, data):
		"""
		Method used to create a tweet in the graph

		@param data: the params of the Tweet we have to create, only has to include the id
		"""
		if "id" not in data.keys():
			log.error("ERROR CREATING A TWEET")
			log.debug("Error: Specified data doesn't contain necessary fields - id")
			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__create_tweet, data)

	def __create_tweet(self, tx, data):
		log.debug("CREATING TWEET")
		try:
			tx.run(f"MERGE (:{TWEET_LABEL} {{id: $id}})", id=str(data["id"]))
		except Exception as e:
			log.exception(f"Error trying to create a Tweet {e}")

	def add_writer_relationship(self, data):
		"""Method used to create a new WRITE relationship

		@param data: The params of the new relationship we want to create. Should include a tweet_id, a user_id and
		the user's type
		"""

		if "tweet_id" not in data.keys() or "user_id" not in data.keys() or "user_type" not in data.keys():
			log.error("ERROR CREATING A WRITE RELATIONSHIP")
			log.error("Error: Specified data doesn't contain necessary fields - tweet_id, user_id, user_type")
			return

		if data["user_type"] not in [BOT_LABEL, USER_LABEL]:
			log.error("ERROR CREATING A WRITE RELATIONSHIP")
			log.error(f"Error: Unacceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")
			return

		with self.driver.session() as session:
			data['label'] = WROTE_LABEL
			data['type_1'] = data['user_type']
			data['id_1'] = data['user_id']
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['tweet_id']

			# Caller for transactional unit of work
			return session.write_transaction(self.__create_relationship, data)

	def add_retweet_relationship(self, data):
		"""Method used to create a new RETWEET relationship

		@param data: The params of the new relationship we want to create. Should include a tweet_id, a user_id and
		the user's type
		"""

		if "tweet_id" not in data.keys() or "user_id" not in data.keys() or "user_type" not in data.keys():
			log.error("ERROR CREATING A RETWEET RELATIONSHIP")
			log.error("Error: Specified data doesn't contain necessary fields - tweet_id, user_id, user_type")
			return

		if data["user_type"] not in [BOT_LABEL, USER_LABEL]:
			log.error("ERROR CREATING A RETWEET RELATIONSHIP")
			log.error(f"Error: Unacceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")
			return

		with self.driver.session() as session:
			data['label'] = RETWEET_LABEL
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['tweet_id']
			data['type_1'] = data['user_type']
			data['id_1'] = data['user_id']

			# Caller for transactional unit of work
			return session.write_transaction(self.__create_relationship, data)

	def add_quote_relationship(self, data):
		"""Method used to create a new QUOTE relationship

		@param data: The params of the new relationship we want to create. Should include a tweet_id and the
		quoted_tweet
		"""

		if "tweet_id" not in data.keys() or "quoted_tweet" not in data.keys():
			log.error("ERROR CREATING A QUOTE RELATIONSHIP")
			log.error("Error: Specified data doesn't contain necessary fields - tweet_id and quoted_tweet")
			log.error(data)
			return

		with self.driver.session() as session:
			data['label'] = QUOTE_LABEL
			data['type_1'] = TWEET_LABEL
			data['id_1'] = data['tweet_id']
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['quoted_tweet']

			# Caller for transactional unit of work
			return session.write_transaction(self.__create_relationship, data)

	def add_reply_relationship(self, data):
		"""Method used to create a new REPLY relationship

		@param data: The params of the new relationship we want to create. Should include a tweet and the reply
		"""
		if "tweet" not in data.keys() or "reply" not in data.keys():
			log.error("ERROR CREATING A REPLY RELATIONSHIP")
			log.error("Error: Specified data doesn't contain necessary fields - tweet and reply")
			return

		with self.driver.session() as session:
			data['label'] = REPLY_LABEL
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['tweet']
			data['type_1'] = TWEET_LABEL
			data['id_1'] = data['reply']

			# Caller for transactional unit of work
			return session.write_transaction(self.__create_relationship, data)

	def add_follow_relationship(self, data):
		"""Method used to create a new FOLLOWS relationship

		@param data: The params of the new relationship we want to create. Should include a type_1, type_2, id_1, id_2
		"""
		if (
				"id_1" not in data.keys()
				or "id_2" not in data.keys()
				or "type_1" not in data.keys()
				or "type_2" not in data.keys()
		):
			log.error("ERROR CREATING A RELATIONSHIP")
			log.error(
				"Error: Specified data doesn't contain necessary fields - type_1, type_to, id_1, id_2"
			)

			return

		if data["type_1"] not in [BOT_LABEL, USER_LABEL] or data["type_2"] not in [
			BOT_LABEL,
			USER_LABEL,
		]:
			log.error("ERROR CREATING A RELATIONSHIP")
			log.error(f"Error: Unacceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			data['label'] = FOLLOW_LABEL
			return session.write_transaction(self.__create_relationship, data)

	def __create_relationship(self, tx, data):
		log.debug(f"CREATING RELATIONSHIP <{data['label']}> betweet {data['id_1']} and {data['id_2']}")

		try:
			result = tx.run(f"MATCH (u: {data['type_1']} {{ id: $id1 }}), (r: {data['type_2']} {{ id: $id2 }}) "
							f"MERGE (u)-[:{data['label']}]->(r)", id1=str(data['id_1']), id2=str(data['id_2']))

			log.debug(f"Created relationship:{result}")
		except Exception as e:
			log.exception(f"Error trying to create a relationship -> {e}")

	def check_bot_exists(self, id):
		"""Method used to check if there exists a bot with a given id

		@param id: The id of the bot we want to check the existance of
		"""

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__bot_exists, id)

	def __bot_exists(self, tx, data):
		log.debug("CHECKING BOT EXISTANCE")

		result = tx.run(f"MATCH (r:{BOT_LABEL} {{ id:$id }}) RETURN r", id=str(data))

		if len(result.data()) == 0:
			return False
		else:
			return True

	def check_user_exists(self, id):
		"""Method used to check if there exists a user with a given id

		@param id: The id of the user we want to check the existance of
		"""

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__user_exists, id)

	def __user_exists(self, tx, data):
		log.debug("CHECKING USER EXISTANCE")

		result = tx.run(f"MATCH (r:{USER_LABEL} {{ id:$id }}) RETURN r", id=str(data))

		if len(result.data()) == 0:
			return False
		else:
			return True

	def check_tweet_exists(self, id):
		"""Method used to check if there exists a tweet with a given id

		@param id: The id of the tweet we want to check the existance of
		"""

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__tweet_exists, id)

	def __tweet_exists(self, tx, data):
		log.debug("CHECKING TWEET EXISTANCE")

		result = tx.run(f"MATCH (r:{TWEET_LABEL} {{ id:$id }}) RETURN r", id=str(data))

		return len(result.data()) != 0

	def update_user(self, data):
		"""Method used to update a given user

		@param data: The id of the user we want to update and the other update params. Should include an old_id
		"""
		if "id" not in data.keys():
			log.error("ERROR CREATING A USER")
			log.error("Error: Specified data doesn't contain necessary fields - old_id")

			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__update_user, data)

	def __update_user(self, tx, data):
		log.debug("UPDATING USER")
		try:
			tx.run(f"MATCH (r: {USER_LABEL} {{ id : $id }}) SET r.username=$username, r.name=$name RETURN r",
				   id=str(data['id']),
				   username=data['username'] if 'username' in data else '',
				   name=data['name'] if 'name' in data else '')
		except Exception as e:
			log.exception(f"Error updating user -> {e}")

	def update_bot(self, data):
		"""Method used to update a given bot

		@param data: The params of the bot we want to update and the other update params. Should include an old_id
		"""
		if "id" not in data.keys():
			log.error("ERROR UPDATING A BOT")
			log.error("Error: Specified data doesn't contain necessary fields - old_id")

			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__update_bot, data)

	def __update_bot(self, tx, data):
		log.debug("UPDATING BOT")

		try:
			tx.run(f"MATCH (r: {BOT_LABEL} {{ id : $id }}) SET r.username=$username, r.name=$name RETURN r",
				   id=str(data['id']),
				   username=data['username'] if 'username' in data else '',
				   name=data['name'] if 'name' in data else '')
		except Exception as e:
			log.exception(f"Error trying to update bot -> {e}")

	def delete_user(self, id):
		"""Method used to delete a given user

		@param id: The id of the user we want to delete
		"""

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__delete_node, USER_LABEL, id)

	def delete_bot(self, id):
		"""Method used to delete a given bot

		@param id: The id of the bot we want to delete
		"""

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__delete_node, BOT_LABEL, id)

	def delete_tweet(self, id):
		"""Method used to delete a given tweet

		@param id: The id of the tweet we want to delete
		"""

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__delete_node, TWEET_LABEL, id)

	def __delete_node(self, tx, type, id):
		log.debug("DELETING NODE")
		try:
			tx.run(f'MATCH (r:{type} {{ id: $id }}) DETACH DELETE r', id=str(id))
		except Exception as e:
			log.exception(f"Error trying to delete node -> {e}")

	def delete_writer_relationship(self, data):
		"""Method used to delete WRITE relationship

		@param data: The params of the new relationship we want to create. Should include a tweet_id, a user_id and
		the user's type
		"""

		if (
				"tweet_id" not in data.keys()
				or "user_id" not in data.keys()
				or "user_type" not in data.keys()
		):
			log.error("ERROR DELETING A WRITE RELATIONSHIP")
			log.error(
				"Error: Specified data doesn't contain necessary fields - tweet_id, user_id, user_type"
			)

			return

		if data["user_type"] not in [BOT_LABEL, USER_LABEL]:
			log.error("ERROR DELETING A WRITE RELATIONSHIP")
			log.error(f"Error: Unacceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

			return

		with self.driver.session() as session:
			data['label'] = WROTE_LABEL
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['tweet_id']
			data['type_1'] = data['user_type']
			data['id_1'] = data['user_id']

			# Caller for transactional unit of work
			return session.write_transaction(self.__delete_rel, data)

	def delete_retweet_relationship(self, data):
		"""Method used to delete RETWEET relationship

		@param data: The params of the new relationship we want to create. Should include a tweet_id, a user_id and
		the user's type
		"""

		if (
				"tweet_id" not in data.keys()
				or "user_id" not in data.keys()
				or "user_type" not in data.keys()
		):
			log.error("ERROR DELETING A RETWEET RELATIONSHIP")
			log.error(
				"Error: Specified data doesn't contain necessary fields - tweet_id, user_id, user_type"
			)

			return

		if data["user_type"] not in [BOT_LABEL, USER_LABEL]:
			log.error("ERROR DELETING A RETWEET RELATIONSHIP")
			log.error(f"Error: Unacceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

			return

		with self.driver.session() as session:
			data['label'] = RETWEET_LABEL
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['tweet_id']
			data['type_1'] = data['user_type']
			data['id_1'] = data['user_id']

			# Caller for transactional unit of work
			return session.write_transaction(self.__delete_rel, data)

	def delete_quote_relationship(self, data):
		"""Method used to delete a new QUOTE relationship

		@param data: The params of the new relationship we want to create. Should include a tweet_id and the
		quoted_tweet
		"""

		if (
				"tweet_id" not in data.keys()
				or "quoted_tweet" not in data.keys()
		):
			log.error("ERROR DELETING A QUOTE RELATIONSHIP")
			log.error(
				"Error: Specified data doesn't contain necessary fields - tweet_id and quoted_tweet"
			)

			return

		with self.driver.session() as session:
			data['label'] = QUOTE_LABEL
			data['type_1'] = TWEET_LABEL
			data['id_1'] = data['tweet_id']
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['quoted_tweet']

			# Caller for transactional unit of work
			return session.write_transaction(self.__delete_rel, data)

	def delete_reply_relationship(self, data):
		"""Method used to DELETE a new REPLY relationship

		@param data: The params of the new relationship we want to create. Should include a tweet and the reply
		"""
		if (
				"tweet" not in data.keys()
				or "reply" not in data.keys()
		):
			log.error("ERROR DELETE A REPLY RELATIONSHIP")
			log.error(
				"Error: Specified data doesn't contain necessary fields - tweet and reply"
			)

			return

		with self.driver.session() as session:
			data['label'] = REPLY_LABEL
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['tweet']
			data['type_1'] = TWEET_LABEL
			data['id_1'] = data['reply']

			# Caller for transactional unit of work
			return session.write_transaction(self.__delete_rel, data)

	def delete_follow_relationship(self, data):
		"""Method used to delete a given bot

		@param data: The params of the new relationship we want to delete. Should include a type_1, type_2, id_1, id_2
		"""
		if (
				"id_1" not in data.keys()
				or "id_2" not in data.keys()
				or "type_1" not in data.keys()
				or "type_2" not in data.keys()
		):
			log.error("ERROR DELETING A RELATIONSHIP")
			log.error(
				"Error: Specified data doesn't contain necessary fields - type_1, type_2, id_1, id_2"
			)

			return

		if data["type_1"] not in [BOT_LABEL, USER_LABEL] or data["type_2"] not in [
			BOT_LABEL,
			USER_LABEL,
		]:
			log.error("ERROR DELETING A RELATIONSHIP")
			log.error(f"Error: Unaceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			data["label"] = FOLLOW_LABEL
			return session.write_transaction(self.__delete_rel, data)

	def __delete_rel(self, tx, data):
		log.debug("DELETING RELATIONSHIP")

		try:
			tx.run(f"MATCH (a:{data['type_1']}{{id: $from_id}})-[r:{data['label']}]->(b:{data['type_2']}{{id: $to_id}})"
				   f"DELETE r",
				   from_id=str(data['id_1']), to_id=str(data['id_2']))
		except Exception as e:
			log.exception(f"Error trying to delete relationship {e}")
			
	def search_tweets(self, tweet=None):
		"""Method used to search for a given tweet

		@param tweet: The params of the bot we want to look for. By default we look for all bots
		"""

		with self.driver.session as session:
			return session.write_transaction(self.__search_tweet, tweet)

	def __search_tweet(self, tx, tweet_id):
		log.debug("SEARCHING TWEET")

		result = []
		for i in tx.run(f"MATCH (r: {TWEET_LABEL} {{id: $id}}) RETURN r", id=str(tweet_id)):
			result.append(dict(i.items()[0][1]))

		return result

	def search_bots(self, data={}):
		"""Method used to search for a given bot

		@param data: The params of the bot we want to look for. By default we look for all bots
		"""

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__search_bots, data)

	@staticmethod
	def __search_bots(tx, data):
		log.debug("SEARCHING BOTS")

		query_filters = "{"
		if "id" in data.keys():
			query_filters += "id: $id,"
			data['id'] = str(data['id'])
		if "name" in data.keys():
			query_filters += "name: '$name',"
		if "username" in data.keys():
			query_filters += "username: '$username',"

		query_filters = (query_filters[:-1] if len(query_filters) > 1 else query_filters) + "}"

		query_result = tx.run(f'MATCH (r:{BOT_LABEL} {query_filters}) RETURN r',
							  data)

		result = []
		for i in query_result:
			result.append(dict(i.items()[0][1]))

		return result

	def search_users(self, data={}):
		"""Method used to search for a given user

		@param data: The params of the user we want to look for. By default we look for all users
		"""

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__search_users, data)

	@staticmethod
	def __search_users(tx, data):
		log.debug("SEARCHING USERS")

		query_filters = "{"
		if "id" in data.keys():
			query_filters += "id: $id,"
			data['id'] = str(data['id'])
		if "name" in data.keys():
			query_filters += "name: '$name',"
		if "username" in data.keys():
			query_filters += "username: '$username',"

		query_filters = (query_filters[:-1] if len(query_filters) > 1 else query_filters) + "}"

		query_result = tx.run(f'MATCH (r:{USER_LABEL} {query_filters}) RETURN r',
							  data)

		result = []
		for i in query_result:
			result.append(dict(i.items()[0][1]))

		return result

	def check_writer_relationship(self, data):
		"""Method used to delete WRITE relationship

		@param data: The params of the new relationship we want to create. Should include a tweet_id, a user_id and
		the user's type
		"""

		if (
				"tweet_id" not in data.keys()
				or "user_id" not in data.keys()
				or "user_type" not in data.keys()
		):
			log.error("ERROR CHECKING A WRITE RELATIONSHIP")
			log.error(
				"Error: Specified data doesn't contain necessary fields - tweet_id, user_id, user_type"
			)

			return

		if data["user_type"] not in [BOT_LABEL, USER_LABEL]:
			log.error("ERROR CHECKING A WRITE RELATIONSHIP")
			log.error(f"Error: Unacceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

			return

		with self.driver.session() as session:
			data['label'] = WROTE_LABEL
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['tweet_id']
			data['type_1'] = data['user_type']
			data['id_1'] = data['user_id']

			# Caller for transactional unit of work
			return session.write_transaction(self.__check_relationship, data)

	def check_retweet_relationship(self, data):
		"""Method used to delete RETWEET relationship

		@param data: The params of the new relationship we want to create. Should include a tweet_id, a user_id and
		the user's type
		"""

		if (
				"tweet_id" not in data.keys()
				or "user_id" not in data.keys()
				or "user_type" not in data.keys()
		):
			log.error("ERROR CHECKING A RETWEET RELATIONSHIP")
			log.error(
				"Error: Specified data doesn't contain necessary fields - tweet_id, user_id, user_type"
			)

			return

		if data["user_type"] not in [BOT_LABEL, USER_LABEL]:
			log.error("ERROR CHECKING A RETWEET RELATIONSHIP")
			log.error(f"Error: Unacceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

			return

		with self.driver.session() as session:
			data['label'] = RETWEET_LABEL
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['tweet_id']
			data['type_1'] = data['user_type']
			data['id_1'] = data['user_id']

			# Caller for transactional unit of work
			return session.write_transaction(self.__check_relationship, data)

	def check_quote_relationship(self, data):
		"""Method used to check a new QUOTE relationship

		@param data: The params of the new relationship we want to check. Should include a tweet_id and the
		quoted_tweet
		"""

		if (
				"tweet_id" not in data.keys()
				or "quoted_tweet" not in data.keys()
		):
			log.error("ERROR CHECKING A QUOTE RELATIONSHIP")
			log.error(
				"Error: Specified data doesn't contain necessary fields - tweet_id and quoted_tweet"
			)
			log.error(data)

			return

		with self.driver.session() as session:
			data['label'] = QUOTE_LABEL
			data['type_1'] = TWEET_LABEL
			data['id_1'] = data['tweet_id']
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['quoted_tweet']

			# Caller for transactional unit of work
			return session.write_transaction(self.__check_relationship, data)

	def check_reply_relationship(self, data):
		"""Method used to check a new REPLY relationship

		@param data: The params of the new relationship we want to create. Should include a tweet and the reply
		"""
		if (
				"tweet" not in data.keys()
				or "reply" not in data.keys()
		):
			log.error("ERROR CHECK A REPLY RELATIONSHIP")
			log.error(
				"Error: Specified data doesn't contain necessary fields - tweet and reply"
			)

			return

		with self.driver.session() as session:
			data['label'] = REPLY_LABEL
			data['type_2'] = TWEET_LABEL
			data['id_2'] = data['tweet']
			data['type_1'] = TWEET_LABEL
			data['id_1'] = data['reply']

			# Caller for transactional unit of work
			return session.write_transaction(self.__check_relationship, data)

	def check_follow_exists(self, data):
		"""Method used to check whether a relationship exists between two IDs

		@param data: The params of the entities involved in the relationshi+ we want to look for. Should include
			a type_1, type_2, id_1, id_2
		"""
		if (
				"id_1" not in data.keys()
				or "id_2" not in data.keys()
				or "type_1" not in data.keys()
				or "type_2" not in data.keys()
		):
			log.error("ERROR CHECKING RELATIONSHIP")
			log.debug(
				"Error: Specified data doesn't contain necessary fields - type_1, type_2, id_1, id_2"
			)

			return

		if data["type_1"] not in [BOT_LABEL, USER_LABEL] or data["type_2"] not in [
			BOT_LABEL,
			USER_LABEL,
		]:
			log.error("ERROR CHECKING RELATIONSHIP")
			log.error(f"Error: Unacceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			data['label'] = FOLLOW_LABEL
			return session.write_transaction(self.__check_relationship, data)

	def __check_relationship(self, tx, data):
		log.debug("VERIFYING RELATIONSHIP EXISTANCE")

		query = f'MATCH (a: {data["type_1"]} {{id: $id1 }})-[r:{data["label"]}]' \
				f'->(b:{data["type_2"]} {{id: $id2 }}) RETURN a, b'

		result = tx.run(query, id1=str(data["id_1"]), id2=str(data["id_2"]))

		return len(result.values()) != 0

	def get_following(self, data):
		"""Method used to find all accounts a given entity is following

		@param data: The specification of who we want to get the followings of. Should include a id and type
		"""
		if "id" not in data.keys():
			log.error("ERROR RETRIEVING FOLLOWINGS")
			log.error(
				"Error: Specified data doesn't contain necessary fields - type, id"
			)

			return

		if 'type' in data and data["type"] not in [BOT_LABEL, USER_LABEL]:
			log.error("ERROR RETRIEVING FOLLOWINGS")
			log.error(f"Error: Unaceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__get_following, data)

	def __get_following(self, tx, data):
		log.debug("GETTING FOLLOWINGS")

		query = f"MATCH (a {':' + data['type'] if 'type' in data else ''} {{id: $id }})-" \
				f"[r:{FOLLOW_LABEL}]->(b) RETURN b"

		result = []
		for i in tx.run(query, id=data['id']):
			entry = dict(i.items()[0][1])
			entry['label'] = list(i.items()[0][1].labels)[0]
			result.append(entry)

		return result

	def get_followers(self, data):
		"""Method used to find all accounts following a given entity

		@param data: The specification of who we want to get the followings of. Should include a id and type
		"""
		if "id" not in data.keys():
			log.error("ERROR RETRIEVING FOLLOWERS")
			log.debug(
				"Error: Specified data doesn't contain necessary fields - type, id"
			)

			return

		if 'type' in data and data["type"] not in [BOT_LABEL, USER_LABEL]:
			log.error("ERROR RETRIEVING FOLLOWINGS")
			log.error(f"Error: Unaceptable specified types. Types must be {BOT_LABEL} or {USER_LABEL}")

			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__get_followers, data)

	def __get_followers(self, tx, data):
		log.debug("GETTING FOLLOWERS")

		query = f'MATCH (b)-[r:{FOLLOW_LABEL}]->' \
				f'(a {":" + data["type"] if "type" in data else ""} {{id: $id }}) RETURN b'

		result = []
		for i in tx.run(query, id=data["id"]):
			entry = dict(i.items()[0][1])
			entry['label'] = list(i.items()[0][1].labels)[0]
			result.append(entry)

		return result

	def export_sample_network(self, export_type="json"):
		if export_type not in ["json", "csv", "graphml"]:
			log.error("ERROR EXPORTING RESULT")
			log.error(
				"Error: ",
				"Specified export type not supported. Please use json, csv or graphml",
			)

			return

		with self.driver.session() as session:
			query = QUERY
			result = session.write_transaction(self.__export_query, export_type, query, False)

			output = result.data()[0]["data"]

			if export_type == "json":
				output = "[" + output.replace("\n", ",") + "]"

			return json.loads(output)

	def export_query(self, query, export_type="json", rel_node_properties=False):
		if export_type not in ["json", "csv", "graphml"]:
			log.error("ERROR EXPORTING RESULT")
			log.error(
				"Error: ",
				"Specified export type not supported. Please use json, csv or graphml",
			)

			return

		with self.driver.session() as session:
			result = session.write_transaction(self.__export_query, export_type, query, rel_node_properties)

			output = result.data()[0]["data"]

			if export_type == "json":
				output = "[" + output.replace("\n", ",") + "]"

			return json.loads(output)

	def __export_query(self, tx, export_type, query, rel_node_properties):
		log.debug("EXPORTING QUERY NETWORK")
		log.debug(query)
		return tx.run(f"CALL apoc.export.{export_type}.query(\"{query}\",null,"
					  f"{{useTypes:true, stream:true, writeNodeProperties:{rel_node_properties}}})")

	def export_network(self, export_type="graphml"):
		"""Method used to export the entire database

		@param export_type: What type we want to export to. Graphml by default
		"""

		if export_type not in ["json", "csv", "graphml"]:
			log.error("ERROR EXPORTING RESULT")
			log.error(
				"Error: ",
				"Specified export type not supported. Please use json, csv or graphml",
			)

			return

		with self.driver.session() as session:
			result = session.write_transaction(self.__export_network, export_type)

			result = result.data()[0]["data"]

			if export_type == "json":
				result = "[" + result.replace("\n", ",") + "]"

			return json.loads(result)

	@staticmethod
	def __export_network(tx, export_type):
		log.debug("EXPORTING NETWORK")

		if export_type == "json":
			result = tx.run("CALL apoc.export.json.all(null,{useTypes:true, stream:true})")
		elif export_type == "csv":
			result = tx.run("CALL apoc.export.csv.all(null,{useTypes:true, stream:true})")
		else:
			result = tx.run("CALL apoc.export.graphml.all(null,{useTypes:true, stream:true})")

		return result

	@staticmethod
	def __node_type(tx, data):
		log.debug("GETTING NODE TYPE")
		query = "match (a {id : $id}) return labels(a)"
		result = tx.run(query, id=data['id'])
		try:
			return list(result)[0].values()[0][0]
		except Exception as e:
			return None

	def node_type(self, data):
		if "id" not in data.keys():
			log.error("ERROR GETTING NODE TYPE")
			log.debug(
				"Error: Specified data doesn't contain necessary fields - type, id"
			)

			return

		with self.driver.session() as session:
			# Caller for transactional unit of work
			return session.write_transaction(self.__node_type, data)

	def __get_entities_stats(self, tx):
		log.debug("GETTING ENTITIES STATS")

		query = "match (b:Bot) with count(b) as counter\
			return 'Bot' as label,counter\
			union all\
			match (t:Tweet) with count(t) as counter\
			return 'Tweet' as label,counter\
			union all\
			match (u:User) with count(u) as counter\
			return 'User' as label,counter"

		return tx.run(query)

	def get_entities_stats(self):
		with self.driver.session() as session:
			return session.write_transaction(self.__get_entities_stats)

	def __get_tweets_written(self, tx, data):
		log.debug("GETTING WRITTEN  TWEETS")

		if 'id' not in data:
			log.error("ERROR GETTING WRITTEN  TWEETS")
			log.error("Error: ", "id not defined.")
			return

		query = "match (a {id: $id})-[:WROTE]->(b) return distinct  b"
		return [d.values()[0]['id'] for d in list(tx.run(query, id=data['id']))]

	def get_tweets_written(self, data):
		with self.driver.session() as session:
			return session.write_transaction(self.__get_tweets_written, data)

	"""
			result = tx.run(f"MATCH (u: {data['type_1']} {{ id: $id1 }}), (r: {data['type_2']} {{ id: $id2 }}) "
						f"MERGE (u)-[:{data['label']}]->(r)", id1=str(data['id_1']), id2=str(data['id_2']))
	"""

	def add_wrote_relationship(self, data):
		"""Method used to create a new WROTE relationship

		@param data: The params of the new relationship we want to create. Should include a tweet and the reply
		"""
		if "user_id" not in data.keys() or "tweet_id" not in data.keys() or 'user_type' not in data.keys():
			log.error("ERROR CREATING A WROTE RELATIONSHIP")
			log.error("Error: Specified data doesn't contain necessary fields - tweet_id, user_id and user_type")
			return

		with self.driver.session() as session:
			data['label'] = WROTE_LABEL
			data['type_1'] = data['user_type']
			data['type_2'] = TWEET_LABEL
			data['id_1'] = data['user_id']
			data['id_2'] = data['tweet_id']

			# Caller for transactional unit of work
			return session.write_transaction(self.__create_relationship, data)


if __name__ == "__main__":
	neo = Neo4jAPI()
	# neo.add_bot({"id":0,"name":"Jonas","username":"Jonas_Pistolas"})
	# neo.add_user({"id":0,"name":"DS","username":"FenixD.S"})
	# neo.add_follow_relationship({"id_1": 0, "id_2": 0, "type_1": BOT_LABEL, "type_2": USER_LABEL})

	# print(neo.check_bot_exists(0))
	# print(neo.check_user_exists(0))

	# neo.update_user({"id": 0, "name": "Diogo Ass"})
	# neo.update_user({"id": 0, "username": "FenixDickSucker","name":"DS"})

	# neo.update_bot({"id":0,"name":"bot lindo"})

	# print(neo.search_bots({"name":"bot lindo"}))
	# print(neo.search_users({"id":0}))
	# print(neo.check_relationship_exists({"id_1": 0, "id_2": 0, "type_1": BOT_LABEL, "type_2": USER_LABEL}))

	# print(neo.get_following({"type": BOT_LABEL, "id": 0}))
	# print(neo.get_followers({"type": USER_LABEL, "id": 0}))

	# print(neo.get_following({"type": "BOT", "id": 0}))
	# print(neo.get_followers({"type": "USER", "id": 0}))

	# neo.export_network()
	# print(neo.export_network("csv"))
	# print()
	# print(neo.export_network("json"))
	# print()
	# print(neo.export_network())

	# neo.export_network()
	# neo.export_network("csv")
	# neo.export_network("json")

	# neo.delete_user(0)
	# neo.delete_follow_relationship({"id_1": 0, "id_2": 0, "type_1": BOT_LABEL, "type_2": USER_LABEL})
	neo.close()
