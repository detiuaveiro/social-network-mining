## @package twitter

import os

from rabbit_messaging import MessagingSettings
import tweepy
from bots.twitter_bot import TwitterBot
from credentials import TASKS_EXCHANGE, TASKS_ROUTING_KEY_PREFIX, TASKS_QUEUE_PREFIX, LOG_EXCHANGE, LOG_ROUTING_KEY, \
	QUERY_EXCHANGE, QUERY_ROUTING_KEY, DATA_EXCHANGE, DATA_ROUTING_KEY, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, VHOST, \
	RABBITMQ_FULL_HTTP_URL, TWEET_EXCHANGE, TWEET_ROUTING_KEY, USER_EXCHANGE, USER_ROUTING_KEY, TWEET_LIKE_EXCHANGE, \
	TWEET_LIKE_ROUTING_KEY, QUERY_FOLLOW_USER_EXCHANGE, QUERY_FOLLOW_USER_ROUTING_KEY, QUERY_TWEET_LIKE_EXCHANGE, \
	QUERY_TWEET_LIKE_ROUTING_KEY, QUERY_TWEET_RETWEET_ROUTING_KEY, QUERY_TWEET_RETWEET_EXCHANGE, \
	QUERY_TWEET_REPLY_EXCHANGE, QUERY_TWEET_REPLY_ROUTING_KEY, QUERY_KEYWORDS_EXCHANGE, QUERY_KEYWORDS_ROUTING_KEY, \
	MAIN_EXCHANGE, MAIN_ROUTING_KEY
from tweepy.binder import bind_api


if __name__ == "__main__":
	bot_id = int(os.environ.get('BOT_ID'))

	messaging_settings = {
		TASKS_EXCHANGE: MessagingSettings(exchange=TASKS_EXCHANGE, routing_key=f"{TASKS_ROUTING_KEY_PREFIX}.{bot_id}",
		                                  queue=f"{TASKS_QUEUE_PREFIX}-{bot_id}"),
		MAIN_EXCHANGE: MessagingSettings(exchange=MAIN_EXCHANGE, routing_key=MAIN_ROUTING_KEY),

		LOG_EXCHANGE: MessagingSettings(exchange=f"{LOG_EXCHANGE}.{bot_id}", routing_key=LOG_ROUTING_KEY),
		QUERY_EXCHANGE: MessagingSettings(exchange=f"{QUERY_EXCHANGE}.{bot_id}", routing_key=QUERY_ROUTING_KEY),
		DATA_EXCHANGE: MessagingSettings(exchange=f"{DATA_EXCHANGE}.{bot_id}", routing_key=DATA_ROUTING_KEY),

		TWEET_EXCHANGE: MessagingSettings(exchange=f"{TWEET_EXCHANGE}.{bot_id}", routing_key=TWEET_ROUTING_KEY),
		USER_EXCHANGE: MessagingSettings(exchange=f"{USER_EXCHANGE}.{bot_id}", routing_key=USER_ROUTING_KEY),
		TWEET_LIKE_EXCHANGE: MessagingSettings(exchange=f"{TWEET_LIKE_EXCHANGE}.{bot_id}", routing_key=TWEET_LIKE_ROUTING_KEY),
		QUERY_FOLLOW_USER_EXCHANGE: MessagingSettings(exchange=f"{QUERY_FOLLOW_USER_EXCHANGE}.{bot_id}",
		                                              routing_key=QUERY_FOLLOW_USER_ROUTING_KEY),
		QUERY_TWEET_LIKE_EXCHANGE: MessagingSettings(exchange=f"{QUERY_TWEET_LIKE_EXCHANGE}.{bot_id}",
		                                             routing_key=QUERY_TWEET_LIKE_ROUTING_KEY),
		QUERY_TWEET_RETWEET_EXCHANGE: MessagingSettings(exchange=f"{QUERY_TWEET_RETWEET_EXCHANGE}.{bot_id}",
		                                                routing_key=QUERY_TWEET_RETWEET_ROUTING_KEY),
		QUERY_TWEET_REPLY_EXCHANGE: MessagingSettings(exchange=f"{QUERY_TWEET_REPLY_EXCHANGE}.{bot_id}",
		                                              routing_key=QUERY_TWEET_REPLY_ROUTING_KEY),
		QUERY_KEYWORDS_EXCHANGE: MessagingSettings(exchange=f"{QUERY_KEYWORDS_EXCHANGE}.{bot_id}",
		                                           routing_key=QUERY_KEYWORDS_ROUTING_KEY),
	}

	proxy_port = os.environ.get('PROXY_PORT', '9050')
	consumer_key = os.environ.get('CONSUMER_KEY', '')
	consumer_secret = os.environ.get('CONSUMER_SECRET', '')
	token = os.environ.get('TOKEN', '')
	token_secret = os.environ.get('TOKEN_SECRET', '')

	proxy = f"socks5h://localhost:{proxy_port}"


	class MYAPI(tweepy.API):
		def __init__(self, auth_handler, wait_on_rate_limit, proxy):
			super().__init__(auth_handler=auth_handler, wait_on_rate_limit=wait_on_rate_limit, proxy=proxy)

		@property
		def home_timeline(self):
			""" :reference: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-home_timeline
				:allowed_param:'since_id', 'max_id', 'count'
			"""
			return bind_api(
				api=self,
				path='/statuses/home_timeline.json',
				payload_type='status', payload_list=True,
				allowed_param=['since_id', 'max_id', 'count', 'tweet_mode'],
				require_auth=True
			)

		@property
		def user_timeline(self):
			""" :reference: https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
				:allowed_param:'id', 'user_id', 'screen_name', 'since_id', 'max_id', 'count', 'include_rts', 'trim_user', 'exclude_replies'
			"""
			return bind_api(
				api=self,
				path='/statuses/user_timeline.json',
				payload_type='status', payload_list=True,
				allowed_param=['id', 'user_id', 'screen_name', 'since_id',
				               'max_id', 'count', 'include_rts', 'trim_user',
				               'exclude_replies', 'tweet_mode']
			)

		@property
		def search(self):
			""" :reference: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
				:allowed_param:'q', 'lang', 'locale', 'since_id', 'geocode',
				 'max_id', 'until', 'result_type', 'count',
				  'include_entities'
			"""
			return bind_api(
				api=self,
				path='/search/tweets.json',
				payload_type='search_results',
				allowed_param=['q', 'lang', 'locale', 'since_id', 'geocode',
				               'max_id', 'until', 'result_type', 'count',
				               'include_entities', 'tweet_mode']
			)


	twitter_auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
	twitter_auth.set_access_token(key=token, secret=token_secret)
	bot = TwitterBot(RABBITMQ_FULL_HTTP_URL, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, VHOST, messaging_settings, bot_id,
	                 MYAPI(auth_handler=twitter_auth, wait_on_rate_limit=True, proxy=proxy))
	bot.run()
