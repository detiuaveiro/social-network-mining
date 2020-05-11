from tweepy.binder import bind_api
import tweepy
import os
from datetime import datetime, timedelta


class MYAPI(tweepy.API):

	def __init__(self, auth_handler, wait_on_rate_limit, proxy):
		super().__init__(auth_handler=auth_handler, wait_on_rate_limit=wait_on_rate_limit, proxy=proxy)

	@property
	def search(self):
		return bind_api(
			api=self,
			path='/search/tweets.json',
			payload_type='search_results',
			allowed_param=['q', 'lang', 'locale', 'since_id', 'geocode',
			               'max_id', 'until', 'result_type', 'count',
			               'include_entities', 'tweet_mode'])


def auth():
	# Credenciais do professor mario antunes
	consumer_key = '2lDgkNXdm03bxodf55vlY5IHo'
	consumer_secret = 'w5SaNzPCLyaBL1ieyGpm4uwjan5Y2GDqQjbbSUoBTT5Fl3cLP4'
	access_token_key = '276620312-0oyEjiC76ouJXCWALH5P9L3NXHSQ7kPw75jL9wse'
	access_token_secret = 'HuJgudHMikT6VGd13M79GkXf0IdzDw20xyePaM8gHRJgg'
	twitter_auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
	twitter_auth.set_access_token(key=access_token_key, secret=access_token_secret)

	proxy = os.environ.get('PROXY', 'socks5h://localhost:9050')
	api = MYAPI(auth_handler=twitter_auth, wait_on_rate_limit=True, proxy=proxy)

	return api


def get_data(query, lang='pt'):
	api = auth()
	data = []

	today = datetime.now()
	for day in range(0, 1):
		current_date = today - timedelta(days=day)
		current_date_minus_one_day = current_date - timedelta(days=1)
		data += api.search(
			q=f'{query} since:{current_date_minus_one_day.strftime("%Y-%m-%d")} until:{current_date.strftime("%Y-%m-%d")}',
			lang=lang, count=100, tweet_mode="extended", geocode="39.557191,-8.1,500km")

	return [d._json for d in data]
