import datetime
import credentials
import psycopg2
import logging
import sys

sys.path.append("..")

log = logging.getLogger("PostgreSQL")
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
	logging.Formatter("[%(asctime)s]:[%(levelname)s]:%(module)s - %(message)s")
)
log.addHandler(handler)


class PostgresAPI:
	"""PostgreSQL

	Encompasses methods used for all API and PDP interactions with our PostgreSQL DB.
	"""

	def __init__(self):
		log.debug("Connecting to PostgreSQL Analysis")
		try:
			# Connect to the PostgreSQL server
			self.conn = psycopg2.connect(
				host=credentials.POSTGRES_URL,
				database=credentials.POSTGRES_DB,
				user=credentials.POSTGRES_USERNAME,
				password=credentials.POSTGRES_PASSWORD
			)

		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def insert_tweet(self, data):
		"""
		Attempts to insert a new Tweet item into the database

		@param data: The data of the item we want to insert. Should have - tweet_id, user_id, likes, retweets
		@return A success or failure message ({success: True/False ; error: None/Error})
		"""
		try:
			cursor = self.conn.cursor()
			cursor.execute(
				"INSERT INTO tweets (timestamp, tweet_id, user_id, likes, retweets) values (DEFAULT,%s,%s,%s,%s);",
				(data["tweet_id"], data["user_id"], data["likes"], data["retweets"]))
			self.conn.commit()
			cursor.close()
		except psycopg2.Error as error:
			self.conn.rollback()

			log.error("ERROR INSERTING NEW TWEET")
			log.error(
				"Error: " + str(error)
			)
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

		return {"success": True}

	def insert_user(self, data):
		"""
		Attempts to insert a new User item into the database

		@param data: The collection we want to insert the document into
		@return A success or failure message ({success: True/False ; error: None/Error})
		"""

		try:
			cursor = self.conn.cursor()
			cursor.execute(
				"INSERT INTO users (timestamp, user_id, followers, following) values (DEFAULT,%s,%s,%s);",
				(data["user_id"], data["followers"], data["following"]))
			self.conn.commit()
			cursor.close()
		except psycopg2.Error as error:
			self.conn.rollback()

			log.error("ERROR INSERTING NEW USER")
			log.error(
				"Error: " + str(error)
			)
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

		return {"success": True}

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

			# result = self.postProcessResults(data, ['timestamp', 'tweet_id', 'likes', 'retweets'])
			result = []  # Array of jsons
			for tuple in data:
				result.append(
					{"timestamp": tuple[0], "tweet_id": tuple[1], "likes": tuple[2], "retweets": tuple[3]})

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

			query = "select timestamp, user_id, followers, following from users "
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
				if "following" in params.keys():
					if control == 1:
						query += " AND "
					query += "following = " + str(params["following"])

				query += ";"

			cursor.execute(query)

			data = cursor.fetchall()

			self.conn.commit()
			cursor.close()

			# result = self.postProcessResults(data, ['timestamp', 'tweet_id', 'likes', 'retweets'])
			result = []  # Array of jsons
			for tuple in data:
				result.append(
					{"timestamp": tuple[0], "user_id": tuple[1], "followers": tuple[2], "following": tuple[3]})

			return {"success": True, "data": result}
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}

	def search_logs(self, params=None, limit=None):
		"""
		Searches and returns all logs if no data is specified, or the specific logs matching the parameters.
		Can also specify the amount of logs to be retrieved.
		Data retrieved is ordered by the most recent

		@param params: The parameters we want to query. Right now only bot_id is supported
		@param limit: An optional parameter specifying the amount of logs to be retrieved

		@return The query's result or error
		"""

		try:
			cursor = self.conn.cursor()

			query = \
				f"select * from logs " \
				f"{'WHERE' if params is not None else ''} " \
				f"{'id_bot=' + str(params['bot_id']) if params is not None and 'bot_id' in params.keys() else ''} " \
				f"ORDER BY timestamp DESC " \
				f"{'limit ' + str(limit) if limit is not None else ''} ;"

			cursor.execute(query)
			print(query)

			data = cursor.fetchall()

			self.conn.commit()
			cursor.close()

			# result = self.postProcessResults(data, ['timestamp', 'tweet_id', 'likes', 'retweets'])
			result = []  # Array of jsons

			for tuple in data:
				result.append(
					{"id_bot": tuple[0], "timestamp": tuple[1], "action": tuple[2]})

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

			query = \
				f"select api.name,policies.name,params,active,id_policy,filter.name, policies.bots from policies " \
				f"   left outer join filter on filter.id=policies.filter " \
				f"   left outer join api on api.id=policies.API_type "

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
				if "bot_id" in params.keys():
					if control == 1:
						query += " AND "
					query += str(params['bot_id']) + '= ANY(policies.bots)'

			query += f"{'limit ' + str(limit) if limit is not None else ''} ;"

			cursor.execute(query)

			data = cursor.fetchall()

			self.conn.commit()
			cursor.close()

			result = []  # Array of jsons
			for tuple in data:
				result.append({
					"API_type": tuple[0], "name": tuple[1], "params": tuple[2], "active": tuple[3],
					"policy_id": tuple[4], "filter": tuple[5], "bots": tuple[6]
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
			cursor.execute(
				"INSERT INTO logs (timestamp, id_bot, action) values (DEFAULT,%s,%s);",
				(data["bot_id"], data["action"]))
			self.conn.commit()
			cursor.close()
		except psycopg2.Error as error:
			self.conn.rollback()

			log.error("ERROR INSERTING NEW LOG")
			log.error(
				"Error: " + str(error)
			)

			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()

			log.error("ERROR INSERTING NEW LOG")
			log.error(
				"Error: " + str(error)
			)

			return {"success": False, "error": error}

		return {"success": True}

	def insert_policy(self, data):
		"""
		Attempts to insert a new Log item into the database

		@param data: The data of the item we want to insert.
		@return A success or failure message ({success: True/False ; error: None/Error})
		"""
		try:
			cursor = self.conn.cursor()

			cursor.execute(f"SELECT * FROM api WHERE name=\'{data['api_name']}\';")
			api_existance = cursor.fetchone()
			if len(api_existance) == 0:
				return {"success": False, "error": "Specified API does not exist"}
			else:
				api_id = api_existance[0]

			cursor.execute(f"SELECT * FROM filter WHERE name=\'{data['filter']}\';")
			filter_existance = cursor.fetchone()
			if len(filter_existance) == 0:
				return {"success": False, "error": "Specified Filter does not exist"}
			else:
				filter_id = filter_existance[0]

			cursor.execute(
				f"SELECT * FROM filter_api WHERE api_id={api_id} AND filter_id={filter_id};")
			api_filter_existence = cursor.fetchone()
			if len(api_filter_existence) == 0:
				return {"success": False, "error": "Specified API-Filter connection does not exist"}

			cursor.execute(
				"INSERT INTO policies (api_type, filter, name, params, active, id_policy, bots) values (%s,%s,%s,%s,%s,%s,%s);",
				(api_id, filter_id, data["name"], data["params"], data["active"], data["policy_id"], data["bots"]))

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

			return {"success": True, "data": result}
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
			cursor = self.conn.cursor()

			api_id = None
			if 'api_name' in params.keys():
				cursor.execute(f"SELECT * FROM api WHERE name=\'{params['api_name']}\';")
				api_existance = cursor.fetchone()
				if len(api_existance) == 0:
					return {"success": False, "error": "Specified API does not exist"}
				else:
					api_id = api_existance[0]

			filter_id = None
			if 'filter' in params.keys():
				cursor.execute(f"SELECT * FROM filter WHERE name=\'{params['filter']}\';")
				filter_existance = cursor.fetchone()
				if len(filter_existance) == 0:
					return {"success": False, "error": "Specified Filter does not exist"}
				else:
					filter_id = filter_existance[0]

			if api_id is not None and filter_id is not None:
				cursor.execute(
					f"SELECT * FROM filter_api WHERE api_id={api_id} AND filter_id={filter_id};")
				api_filter_existence = cursor.fetchone()
				if len(api_filter_existence) == 0:
					return {"success": False, "error": "Specified API-Filter connection does not exist"}

			query = f"update policies "

			query += " SET "
			control = 0
			if "api_type" in params.keys():
				query += 'api_type=' + str(api_id)
				control = 1
			if "filter" in params.keys():
				if control == 1:
					query += " , "
				query += 'filter=' + str(filter_id)
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
			if "policy_id" in params.keys():
				if control == 1:
					query += " AND "
				query += 'id_policy=' + str(params['policy_id'])
				control = 1
			if "bot_id" in params.keys():
				if control == 1:
					query += " , "
				query += 'bots=' + str(params['bots'])

			query += f" WHERE id_policy = {policy_id}"
			cursor.execute(query)

			self.conn.commit()
			cursor.close()

			return {"success": True, "data": result}
		except psycopg2.Error as error:
			self.conn.rollback()
			return {"success": False, "error": error}
		except Exception as error:
			self.conn.rollback()
			return {"success": False, "error": error}


if __name__ == "__main__":
	# TODO: Test and implement searching by timestamp ; Policies API
	anal = PostgresAPI()
	'''
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

	print(anal.insert_policy({
	'api_name': 'Twitter', 'filter': 'Keywords', 'name': 'Jonas Pistolas found Ded', 'bots': [1129475305444388866],
	'params': ['OMG'], 'active': True, 'policy_id': 420}))'''

	result = anal.search_policies({'policy_id': 420})
	if result["success"]:
		for i in result["data"]:
			print(i)
	else:
		print(result["error"])
