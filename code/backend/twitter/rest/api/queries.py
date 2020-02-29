import logging
from datetime import datetime

from api.models import Tweet
import api.serializers as serializers


logger = logging.getLogger('queries')


def twitter_tweets(limit=None):
	try:
		all_tweets = Tweet.objects.all()
		data = [
			serializers.Tweet(tweet).data
			for tweet in (all_tweets if not limit or limit > len(all_tweets) else all_tweets[:limit])
		]
		return True, data, "Sucesso a obter todos os tweets"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
		return False, None, "Erro a obter todos os tweets"
