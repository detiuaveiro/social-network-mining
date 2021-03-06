## @package twitter.wrappers
# coding: UTF-8

import psycopg2
import logging

import credentials as credentials
from api.enums import Policy as enum_policy
import django.dispatch

log = logging.getLogger("PostgreSQL")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open("postgres.log", "w"))
handler.setFormatter(
	logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)

signal = django.dispatch.Signal(providing_args=["table_name"])


class PostgresAPI:
	"""PostgreSQL

	Encompasses methods used for all API and PDP interactions with our PostgreSQL DB.
	"""

	def __init__(self):
		log.debug(f"Connecting to PostgreSQL Analysis with credentials: \n"
		          f"url={credentials.POSTGRES_URL}\n"
		          f"db={credentials.POSTGRES_DB}\n"
		          f"user={credentials.POSTGRES_USERNAME}\n"
		          f"port={credentials.POSTGRES_PORT}")
		try:
			# Connect to the PostgreSQL server
			self.conn = psycopg2.connect(
				host=credentials.POSTGRES_URL, database=credentials.POSTGRES_DB,
				user=credentials.POSTGRES_USERNAME, password=credentials.POSTGRES_PASSWORD,
				port=credentials.POSTGRES_PORT
			)

			self.api_types = [x[0] for x in enum_policy.api_types()]
			self.filters = [x[0] for x in enum_policy.api_filter()]
			self.list_of_users = []
			self.list_of_tweets = []

		except (Exception, psycopg2.DatabaseError) as error:
			log.exception(f"Error <{error}> trying to connect to database: ")

	def insert_tweet(self, data):
		self.list_of_tweets.append(data)

	def __save_tweet(self, data):
		"""
		Attempts to insert a new Tweet item into the database

		@param data: The data of the item we want to insert. Should have - tweet_id, user_id, likes, retweets
		@return A success or failure message ({success: True/False ; error: None/Error})
		"""
		try:
			cursor = self.conn.cursor()
			cursor.execute(
				"INSERT INTO tweets (timestamp, tweet_id, user_id, likes, retweets) values (DEFAULT,%s,%s,%s,%s);",
				(int(data["tweet_id"]), int(data["user_id"]), data["likes"], data["retweets"]))
			self.conn.commit()
			signal.send(sender=PostgresAPI, table_name="TweetStats")
			cursor.close()
		except psycopg2.Error as error:
			self.conn.rollback()

			log.exception(f"ERROR <{error}> INSERTING NEW TWEET <{data}>: ")
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

		return {"success": True}

	def insert_user(self, data):
		self.list_of_users.append(data)

	def __save_user(self, data):
		"""
		Attempts to insert a new User item into the database

		@param data: The collection we want to insert the document into
		@return A success or failure message ({success: True/False ; error: None/Error})
		"""

		try:
			cursor = self.conn.cursor()
			cursor.execute(
				"INSERT INTO users (timestamp, user_id, followers, following, protected) values (DEFAULT,%s,%s,%s,%s);",
				(data["user_id"], data["followers"], data["following"], data["protected"])
			)
			self.conn.commit()
			signal.send(sender=PostgresAPI, table_name="users")
			cursor.close()
		except psycopg2.Error as error:
			self.conn.rollback()

			log.exception(f"ERROR <{error}> INSERTING NEW USER <{data}>: ")
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

		return {"success": True}

	def save_all(self):
		"""Method to bulk save all tweets and users"""
		for tweet in self.list_of_tweets:
			self.__save_tweet(tweet)
		self.list_of_tweets = []

		log.info("Save all tweets")

		for user in self.list_of_users:
			self.__save_user(user)	
		self.list_of_users = []

		log.info("Save all users")

	def search_tweet(self, params=None):
		"""
		Searches and returns all Tweets if no data is specified, or the specific tweet matching the given parameters

		@param params: The parameters we want to query
		@return The query's result or error
		"""

		try:
			cursor = self.conn.cursor()

			query = "select timestamp, tweet_id, likes, retweets from tweets "
			if params is None:
				query += ";"
			else:
				query += "WHERE "
				control = 0
				if "tweet_id" in params.keys():
					query += "tweet_id = " + str(params["tweet_id"])
					control = 1
				if "likes" in params.keys():
					if control == 1:
						query += " AND "
					query += "likes = " + str(params["likes"])
					control = 1
				if "retweets" in params.keys():
					if control == 1:
						query += " AND "
					query += "retweets = " + str(params["retweets"])

				query += ";"

			cursor.execute(query)

			data = cursor.fetchall()

			self.conn.commit()
			cursor.close()

			result = []  # Array of jsons
			for tuple in data:
				result.append(
					{"timestamp": tuple[0], "tweet_id": int(tuple[1]), "likes": tuple[2], "retweets": tuple[3]})

			return {"success": True, "data": result}
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

	def search_user(self, params=None):
		"""
		Searches and returns all Users if no data is specified, or the specific tweet matching the given parameters

		@param params: The parameters we want to query
		@return The query's result or error
		"""

		try:
			cursor = self.conn.cursor()

			query = "select timestamp, user_id, followers, following, protected from users "
			if params is None:
				query += ";"
			else:
				query += "WHERE "
				control = 0
				if "user_id" in params.keys():
					query += "user_id = " + str(params["user_id"])
					control = 1
				if "followers" in params.keys():
					if control == 1:
						query += " AND "
					query += "followers = " + str(params["followers"])
					control = 1
				if "protected" in params.keys():
					if control == 1:
						query += " AND "
					query += "protected = " + str(params["followers"])
					control = 1
				if "following" in params.keys():
					if control == 1:
						query += " AND "
					query += "following = " + str(params["following"])

				query += ";"

			cursor.execute(query)

			data = cursor.fetchall()

			self.conn.commit()
			cursor.close()

			result = []  # Array of jsons
			for tuple in data:
				result.append({"timestamp": tuple[0], "user_id": int(tuple[1]), "followers": tuple[2],
				               "following": tuple[3], "protected": tuple[4]})

			return {"success": True, "data": result}
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

	def search_logs(self, params=None, limit=None):
		"""
		Searches and returns all logs if no data is specified, or the specific logs matching the parameters. Can also
		specify the amount of logs to be retrieved. Data retrieved is ordered by the most recent

		@param params: The parameters we want to query. Right now only bot_id is supported
		@param limit: An optional parameter specifying the amount of logs to be retrieved

		@return The query's result or error
		"""

		try:
			cursor = self.conn.cursor()

			query = "select id_bot, action, target_id, timestamp from logs "

			if params is not None:
				query += "WHERE "
				if "bot_id" in params:
					query += f"id_bot={params['bot_id']} AND "
				if "target_id" in params:
					query += f"target_id={params['target_id']} AND "
				if "action" in params:
					query += f"action='{params['action']}' AND "
				if "timestamp" in params:
					query += f"timestamp>'{params['timestamp']}' AND "
				query = query[:-4]

			query += f"ORDER BY timestamp DESC " \
			         f"{'limit ' + str(limit) if limit is not None else ''} ;"

			cursor.execute(query)

			data = cursor.fetchall()

			self.conn.commit()
			cursor.close()

			result = []  # Array of jsons

			for tuple in data:
				result.append(
					{"bot_id": int(tuple[0]), "action": tuple[1], "target_id": int(tuple[2]), "timestamp": tuple[3]})

			return {"success": True, "data": result}
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

	def search_notifications(self, params=None):
		try:
			cursor = self.conn.cursor()

			query = "select notifications.email,notifications.status from notifications"

			if params is not None:
				query += " WHERE true"
				if "email" in params.keys():
					query += f" AND notifications.email='{params['email']}'"

				if "status" in params.keys():
					query += f" AND notifications.status={params['status']}"

			cursor.execute(query)

			data = cursor.fetchall()

			self.conn.commit()
			cursor.close()

			result = []  # Array of jsons

			for entry in data:
				result.append({'email': entry[0], 'status': entry[1]})

			return {"success": True, "data": result}
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

	def search_policies(self, params=None, limit=None):
		"""
		Searches and returns all policies if no data is specified, or the specific policies matching the parameters.
		Can also specify the amount of poliecies to be retrieved.

		@param params: The parameters we want to query. Right now only bot_id is supported
		@param limit: An optional parameter specifying the amount of logs to be retrieved

		@return The query's result or error
		"""

		try:
			cursor = self.conn.cursor()

			query = f"select policies.api_type,policies.name,params,active,id_policy,policies.filter, policies.bots " \
			        f"from policies"

			if params is not None:
				query += " WHERE "
				control = 0
				if "policy_id" in params.keys():
					query += 'policies.id_policy=' + str(params['policy_id'])
					control = 1
				if "api_name" in params.keys():
					if control == 1:
						query += " AND "
					query += 'api.name=\'' + params['api_name'] + '\''
					control = 1
				if "filter" in params.keys():
					if control == 1:
						query += " AND "
					query += f"policies.filter='{params['filter']}'"
					control = 1
				if "bot_id" in params.keys():
					if control == 1:
						query += " AND "
					query += str(params['bot_id']) + '= ANY(policies.bots)'

				if "name" in params.keys():
					if control == 1:
						query += " AND "
					query += f"policies.name='{params['name']}'"


			query += f"{'limit ' + str(limit) if limit is not None else ''} ;"

			cursor.execute(query)

			data = cursor.fetchall()

			self.conn.commit()
			cursor.close()

			result = []  # Array of jsons
			for tuple in data:
				result.append({
					"API_type": tuple[0], "name": tuple[1], "params": tuple[2], "active": tuple[3],
					"policy_id": int(tuple[4]), "filter": tuple[5], "bots": [int(t) for t in tuple[6]]
				})

			return {"success": True, "data": result}
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

	def insert_log(self, data):
		"""
		Attempts to insert a new Log item into the database

		@param data: The data of the item we want to insert. Should have
		@return A success or failure message ({success: True/False ; error: None/Error})
		"""
		try:
			cursor = self.conn.cursor()

			bot_id = int(data['bot_id'])

			insertion_query = "INSERT INTO logs "
			if "target_id" in data:
				insertion_query += \
					f"(id_bot, action, target_id) values {(bot_id, data['action'], int(data['target_id']))};"
			else:
				insertion_query += f"(id_bot, action) values {(bot_id, data['action'])}; "

			cursor.execute(insertion_query)
			log.debug(f"Inserted log <{insertion_query}> on database")
		except psycopg2.Error as error:
			self.conn.rollback()

			log.exception(f"ERROR <{error}> INSERTING NEW LOG <{data}>: ")
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()

			log.exception(f"ERROR <{error}> INSERTING NEW LOG <{data}>: ")
			return {"success": False, "error": error}

		self.conn.commit()
		cursor.close()

		try:
			signal.send(sender=PostgresAPI, table_name="Log")
		except Exception as error:
			log.exception(f"ERROR <{error}> when signaling rest to update cache")

		return {"success": True}

	def insert_policy(self, data):
		"""
		Attempts to insert a new Log item into the database

		@param data: The data of the item we want to insert.
		@return A success or failure message ({success: True/False ; error: None/Error})
		"""

		try:

			if data['api_name'] not in self.api_types:
				return {"success": False, "error": "Specified API does not exist"}

			if data['filter'] not in self.filters:
				return {"success": False, "error": "Specified Filter does not exist"}

			cursor = self.conn.cursor()

			cursor.execute('select max(id_policy) from policies;')
			max_id = cursor.fetchall()[0][0]

			cursor.execute(
				"INSERT INTO policies (api_type, filter, name, params, active, id_policy, bots) "
				"values (%s,%s,%s,%s,%s,%s,%s);",
				(data['api_name'], data['filter'], data["name"], data["params"], data["active"], max_id + 1,
				 data["bots"]))

			self.conn.commit()
			cursor.close()
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

		return {"success": True}

	def delete_policy(self, policy_id):
		"""
		Deletes the policy with the given id

		@param policy_id: The id of the policy we want to delete
		@param limit: An optional parameter specifying the amount of logs to be retrieved

		@return The query's result or error
		"""

		try:
			cursor = self.conn.cursor()

			query = f"delete from policies where id_policy={policy_id};"
			cursor.execute(query)

			self.conn.commit()
			cursor.close()

			return {"success": True}
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

	def update_policy(self, policy_id, params):
		"""
		Updates the policy with the specified policy id, changing the params specified.

		@param params: The parameters we want to update.
		@param policy_id: The id of the policy we want to update
		@param limit: An optional parameter specifying the amount of logs to be retrieved

		@return The query's result or error
		"""

		try:

			if 'api_name' in params.keys():
				if params['api_name'] not in self.api_types:
					return {"success": False, "error": "Specified API does not exist"}

			if 'filter' in params.keys():
				if params['filter'] not in self.filters:
					return {"success": False, "error": "Specified Filter does not exist"}

			cursor = self.conn.cursor()
			query = f"update policies "

			query += " SET "
			control = 0
			if "api_type" in params.keys():
				query += f"api_type='{params['api_name']}'"
				control = 1
			if "filter" in params.keys():
				if control == 1:
					query += " , "
				query += f"filter='{params['filter']}'"
				control = 1
			if "name" in params.keys():
				if control == 1:
					query += " , "
				query += 'name=\'' + str(params['name']) + '\''
				control = 1
			if "params" in params.keys():
				if control == 1:
					query += " , "
				query += 'params=' + str(params['params'])
				control = 1
			if "active" in params.keys():
				if control == 1:
					query += " , "
				query += 'active=' + str(params['active'])
				control = 1
			if "bot_id" in params.keys():
				if control == 1:
					query += " , "
				query += 'bots=' + str(params['bots'])

			query += f" WHERE id_policy = {policy_id}"
			cursor.execute(query)

			self.conn.commit()
			cursor.close()

			return {"success": True}
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

	def update_notifications_status(self):
		cursor = self.conn.cursor()
		query = "update notifications set status='f' where status='t'"
		try:
			cursor.execute(query)
			self.conn.commit()
			cursor.close()
			return {"success": True}
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}


if __name__ == "__main__":
	# TODO: Test and implement searching by timestamp ; Policies API
	anal = PostgresAPI()
	"""
	anal.insert_tweet({"tweet_id": 831606548300517377, "user_id": 6253282, "likes": 100, "retweets": 2})
	anal.insert_user({"user_id": 6253283, "followers": 10000, "following": 1234})
	for i in anal.search_tweet()["data"]:
		print(i)

	for i in anal.search_user()["data"]:
		print(i)

	result = anal.search_policies({'api_name': 'Twitter', 'policy_id': 80, 'bot_id': 1129475305444388866}, limit=10)
	if result["success"]:
		for i in result["data"]:
			print(i)
	else:
		print(result["error"])

	anal.insert_log({"bot_id": 1129475305444388866, "action": "SAVING TWEET (1127597365978959872)"})
	anal.insert_log({"user_id": 1129475305444388866, "action": "SAVING TWEET (1127597365978959872)"})

	print(anal.insert_policy({'api_name': 'Twitter', 'filter': 'Keywords', 'name': 'Jonas Pistolas found Ded', 
							'bots': [1129475305444388866], 'params': ['OMG'], 'active': True, 'policy_id': 421}))
	print(anal.update_policy(421, {'api_name': 'Instagram', 'filter': 'Target'}))
	
	result = anal.search_policies({'policy_id': 421})
	print(result)
	if result["success"]:
		for i in result["data"]:
			print(i)
	else:
		print(result["error"])
	"""
