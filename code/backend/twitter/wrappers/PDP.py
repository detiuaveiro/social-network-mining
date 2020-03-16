import datetime
import json
import random
import sys

sys.path.append('../wrappers')
from mongo_wrapper import *
from neo4j_wrapper import *
from postgresql_wrapper import *
from enums import *
from credentials import *

# Constants used below for the Heuristics
THRESHOLD_LIKE = 0.4
THRESHOLD_RETWEET = 0.6
POLICY_KEYWORDS_MATCHES = 0.2
POLICY_USER_IS_TARGETED = 0.4
PENALTY_LIKED_RECENTLY_SMALL = -0.35
PENALTY_LIKED_RECENTLY_SMALL_INTERVAL = 10
PENALTY_LIKED_RECENTLY_LARGE = -0.65
PENALTY_LIKED_RECENTLY_LARGE_INTERVAL = 5
PENALTY_RETWEETED_USER_RECENTLY = -0.5
PENALTY_RETWEETED_USER_RECENTLY_INTERVAL = 43200
BOT_FOLLOWS_USER = 0.3
BOT_RETWEETED_TWEET = 0.2
BOT_LIKED_TWEET = 0.3


class PDP:
	def __init__(self):
		'''
		Here starts the connections with the other DB wrappers
		'''
		self.mongo = MongoAPI()
		self.neo4j = Neo4jAPI()
		self.postgres = PostgresAPI()
		pass

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
		if msg["type"] == PoliciesTypes.REQUEST_TWEET_LIKE:
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

		elif msg["type"] == PoliciesTypes.REQUEST_TWEET_RETWEET:
			'''
			bot_id
			user_id
			tweet_id
			tweet_text
			tweet_entities
				- from entities, fetch hashtags and mentions
			'''
			res = self.analyze_tweet_retweet(msg)
			evaluate_answer = res > THRESHOLD_LIKE

		elif msg["type"] == PoliciesTypes.REQUEST_TWEET_REPLY:
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
			res = self.analyze_tweet_reply(msg)
			evaluate_answer = True

		elif msg["type"] == PoliciesTypes.REQUEST_FOLLOW_USER:
			'''
			bot_id
			user_id

			workflow of this request:

			1- Check bot and its policies
				1.1- if filter=target and target=tweet_user_id:
						return PERMIT
				1.2- if other_bots.filter=target and other_bots.target=tweet_user_id:
						return DENY
				1.3- No one has this target
						GOTO Rule 2

			2- Check neo4j
				2.1- Bot already follows tweet_user_id (this case should never happen, just here for precaution)
						return DENY
				2.2- Other bot is following tweet_user_id: (questionable, should be discussed)
						return DENY
				2.3- No one follows tweet_user_id:
						return PERMIT
			'''
			evaluate_answer = self.analyze_follow_user(msg)

		if evaluate_answer:
			return self.send_response({"response": "PERMIT"})
		else:
			return self.send_response({"response": "DENY"})

	def send_response(self, msg):
		# json dumps da decisão
		message = json.dumps(msg)
		return message

	def get_first_time_list(self):
		"""
		When a bot connects for the first time to Twitter, he'll have to start following people This is the old way:
		having a set list of possible users and the bot will follow a random group from those followers In future
		iterations we may alter this so that there are possible branches a bot could start with: politics,
		football fan, etc., each branch with a list of possible users to follow

		@return: List of users the bot will start following
		"""
		num_users = random.randint(2, 10)
		users = [
			"dailycristina", "PaulaNevesD", "doloresaveiro", "Corpodormente", "Manzarra",
			"Feromonas", "DanielaRuah", "RicardoTPereira", "LuciaMoniz", "D_Morgado",
			"ClaudiaPFVieira", "RuiSinelCordes", "DiogoBeja", "blackmirror", "13ReasonsWhy",
			"NetflixPT", "DCComics", "gameofthrones", "cw_arrow", "CW_TheFlash",
			"TheCW_Legends", "nbcthisisus", "lacasadepapel", "lucifernetflix",
			"thecwsupergirl", "cw_riverdale", "hawaiifive0cbs", "cwthe100", "agentsofshield",
			"thesimpsons", "macgyvercbs", "americancrimetv", "acsfx", "shadowhunterstv",
			"theamericansfx", "crimminds_cbs", "KimKardashian", "khloekardashian",
			"kourtneykardash", "KendallJenner", "KylieJenner", "KrisJenner", "pewdiepie",
			"tim_cook", "elonmusk", "BillGates", "FCPorto", "KDTrey5", "Cristiano",
			"hazardeden10", "PauDybala_JR", "Sporting_CP", "Dame_Lillard", "stephenasmith",
			"RealSkipBayless", "ManCity", "juventusfc", "FCBarcelona", "realmadrid",
			"SergioRamos", "KingJames", "katyperry", "cher", "NICKIMINAJ", "deadmau5",
			"kanyewest", "axlrose", "patrickcarney", "vincestaples", "KillerMike",
			"thedavidcrosby", "samantharonson", "Eminem", "pittyleone", "thesonicyouth", "bep",
			"ladygaga", "coldplay", "britneyspears", "backstreetboys", "chilipeppers",
			"fosterthepeople", "acdc", "arcticmonkeys", "blurofficial", "gorillaz", "greenday",
			"linkinpark", "MCRofficial", "falloutboy", "PanicAtTheDisco", "AllTimeLow",
			"PTXofficial", "kirstin", "StephenCurry30", "NBA", "SLBenfica", "partido_pan",
			"ppdpsd", "psocialista", "_cdspp", "cdupcppev", "realdonaldtrump", "borisjohnson",
			"nigel_farage", "jeremycorbyn", "theresa_may", "joebiden", "fhollande",
			"angelamerkeicdu", "barackobama", "berniesanders", "nicolasmaduro", "vp",
			"realxi_jinping", "mlp_officiel", "jguaido", "RuiRioPSD", "antoniocostapm",
			"catarina_mart", "cristasassuncao", "heloisapolonia", "jairbolsonaro"
		]

		bot_list = []
		while len(bot_list) < num_users:
			index = random.randint(0, len(users) - 1)
			bot_list.append(users.pop(index))

		return bot_list

	def _bot_is_targeted(self, policy, data):
		"""
		Private function to check if a bot is being targeted in a policy
		Checks first if the bot was mentioned in the tweet, or if the user who posted the tweet is himself listed
		in the policy

		@param Policy dictionary containing its information
		@param Data dictionary containing important information

		@returns True or False depending if the bot was indeed targeted
		"""
		for mentions in data["tweet_entities"]["user_mentions"]:
			if mentions["screen_name"] in policy["bots"]:
				return True

		user = self.mongo.find(
			collection="users",
			query={"id": data["user_id"]},
			single=True
		)
		return user in policy["bots"]

	def _tweet_has_keywords(self, policy, data):
		"""
		Private function to check if a tweet uses any important keywords, be it hashtags or commonly found words

		@param Policy dictionary containing its information
		@param Data dictionary containing important information

		@returns True or False depending if the tweet has keywords
		"""
		for hashtag in data["tweet_entities"]["hashtags"]:
			if hashtag["text"] in policy["params"]:
				return True

		for keyword in policy["params"]:
			if keyword in data["tweet_text"]:
				return True

		return False

	def analyze_tweet_like(self, data):
		"""
		Algorithm to analyse if a bot should like a Tweet
		Takes the current statistics and turns them into a real value

		@param: data - dictionary containing the data of the bot and the tweet it wants to like
		@returns: float that will then be compared to the threshold previously defined
		"""

		heuristic_value = 0
		# Verify if there's a relation between the bot and the user
		type1 = "Bot" if self.neo4j.check_bot_exists(data["bot_id"]) else "User"
		type2 = "Bot" if self.neo4j.check_bot_exists(data["user_id"]) else "User"
		relation_exists = self.neo4j.check_relationship_exists({
			"id_1": data["bot_id"],
			"type_1": type1,
			"id_2": data["user_id"],
			"type_2": type2
		})
		if relation_exists:
			heuristic_value += BOT_FOLLOWS_USER

		# Next we check if the bot and the user have some policies in common
		policy_list = self.postgres.search_policies({
			"bot_id": data["bot_id"]
		})

		if policy_list['success']:
			for policy in policy_list["data"]:

				if policy["filter"] == "Target":
					# Check if our bot is being targeted

					if self._bot_is_targeted(policy, data):
						heuristic_value += POLICY_USER_IS_TARGETED

				elif policy["filter"] == "Keywords":
					# Check if tweet has any important keywords (be it a hashtag or a commonly found word)

					if self._tweet_has_keywords(policy, data):
						heuristic_value += POLICY_KEYWORDS_MATCHES

		# We then check if the bot has retweeted the tweet
		bot_logs = self.postgres.search_logs({"bot_id": data["bot_id"]})
		for log in bot_logs['data']:
			# Log Structure: "ACTION: bot_id and tweet_id
			log_elems = log['action'].split(": ")
			if len(log_elems) != 2:
				continue
			action, users = log_elems
			if "RETWEET" == action:
				bot, tweet = users.split(" and ")
				if tweet == data["tweet_id"]:
					heuristic_value = heuristic_value + BOT_RETWEETED_TWEET if heuristic_value < 0.8 else 1
					break
			elif "TWEET LIKE" == action:
				bot, tweet = users.split(" and ")
				user_tweet = self.mongo.find(
					collection="tweets",
					query={"id": tweet},
					single=True
				)
				if user_tweet == data["user_id"]:
					date = log["timestamp"]
					now = datetime.datetime.now()
					if (now - date).seconds < PENALTY_LIKED_RECENTLY_LARGE_INTERVAL:
						heuristic_value += PENALTY_LIKED_RECENTLY_LARGE
					elif (now - date).seconds < PENALTY_LIKED_RECENTLY_SMALL_INTERVAL:
						heuristic_value += PENALTY_LIKED_RECENTLY_SMALL

		return heuristic_value

	def analyze_tweet_retweet(self, data):

		"""
		Algorithm to analyse if a bot should retweet a Tweet
		Takes the current statistics and turns them into a real value

		@param: data - dictionary containing the data of the bot and the tweet it wants to like
		@returns: float that will then be compared to the threshold previously defined
		"""

		heuristic_value = 0
		# Verify if there's a relation between the bot and the user
		type1 = "Bot" if self.neo4j.check_bot_exists(data["bot_id"]) else "User"
		type2 = "Bot" if self.neo4j.check_bot_exists(data["user_id"]) else "User"
		relation_exists = self.neo4j.check_relationship_exists({
			"id_1": data["bot_id"],
			"type_1": type1,
			"id_2": data["user_id"],
			"type_2": type2
		})

		# Next we check if the bot and the user have some policies in common
		policy_list = self.postgres.search_policies({
			"bot_id": data["bot_id"]
		})

		if policy_list['success']:
			for policy in policy_list['data']:
				if policy["filter"] == "Target":
					# Check if our bot is being targeted

					if self._bot_is_targeted(policy, data):
						heuristic_value += POLICY_USER_IS_TARGETED

				elif policy["filter"] == "Keywords":
					# Check if tweet has any important keywords (be it a hashtag or a commonly found word)

					if self._tweet_has_keywords(policy, data):
						heuristic_value += POLICY_KEYWORDS_MATCHES

		# We then check if the bot has retweeted the tweet
		bot_logs = self.postgres.search_logs({"bot_id": data["bot_id"]})
		for log in bot_logs['data']:
			# Log Structure: "ACTION: bot_id and tweet_id
			log_elems = log['action'].split(": ")
			if len(log_elems) != 2:
				continue
			action, users = log_elems
			if "TWEET LIKE" == action:
				bot, tweet = users.split(" and ")
				if tweet == data["tweet_id"]:
					heuristic_value = heuristic_value + BOT_LIKED_TWEET if heuristic_value < 0.7 else 1
					break
			elif "RETWEET" == action:
				bot, tweet = users.split(" and ")
				user_tweet = self.mongo.find(
					collection="tweets",
					query={"id": tweet},
					single=True
				)
				if user_tweet == data["user_id"]:
					date = log["timestamp"]
					now = datetime.datetime.now()
					if (now - date).seconds < PENALTY_RETWEETED_USER_RECENTLY_INTERVAL:
						heuristic_value += PENALTY_RETWEETED_USER_RECENTLY

		return heuristic_value

	def analyze_tweet_reply(self, data):
		"""
		Algorithm to analyse if a bot should reply
		Takes the current statistics and turns them into a real value

		@param: data - dictionary containing the data of the bot and the tweet it wants to like
		@returns: float that will then be compared to the threshold previously defined
		"""
		# This was not implemented last year
		return 0

	def analyze_follow_user(self, data):
		"""
		Algorithm to analyse if a bot should follow
		Takes the current statistics and turns them into a real value

		@param: data - dictionary containing the data of the bot and the tweet it wants to like
		@returns: float that will then be compared to the threshold previously defined
		"""
		# This was not implemeneted last year
		return False

	def close(self):
		self.neo4j.close()