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


def twitter_tweet(id):
	try:
		Tweet.objects.get(tweet_id=id)
		all_tweets = Tweet.objects.filter(tweet_id=id)
		return True, [serializers.Tweet(tweet).data for tweet in all_tweets], "Sucesso a obter todos os tweets"
	except Tweet.DoesNotExist:
		return False, None, f"O id {id} não existe na base de dados"
	except Exception as e:
		logger.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {e}")
		return False, None, f"Erro a obter todos os tweets do id {id}"
