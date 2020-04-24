from enum import IntEnum


class ServerToBot(IntEnum):
	"""
	Enum for the tasks the bot is able to run. Received by the bot from the server.
	"""
	FOLLOW_USERS = 1
	FIND_BY_KEYWORDS = 2
	LIKE_TWEETS = 3
	RETWEET_TWEETS = 4
	POST_TWEET = 5
	FIND_FOLLOWERS = 6
	KEYWORDS = 7
	GET_TWEET_BY_ID = 8
	GET_USER_BY_ID = 9

	def __str__(self):
		return self.name


class BotToServer(IntEnum):
	"""
	Enum for the Messages sent by the bot to the server.
	"""
	EVENT_USER_FOLLOWED = 1
	EVENT_TWEET_LIKED = 2
	EVENT_TWEET_RETWEETED = 3
	EVENT_TWEET_REPLIED = 4
	QUERY_TWEET_LIKE = 5
	QUERY_TWEET_RETWEET = 6
	QUERY_TWEET_REPLY = 7
	QUERY_FOLLOW_USER = 8
	SAVE_USER = 9
	SAVE_TWEET = 10
	EVENT_USER_BLOCKED = 11
	SAVE_FOLLOWERS = 12
	SAVE_DIRECT_MESSAGES = 13

	QUERY_KEYWORDS = 14

	def __str__(self):
		return self.name
