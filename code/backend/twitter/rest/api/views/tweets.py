from rest_framework.decorators import api_view
from rest_framework.status import *

from api.views.utils import create_response
import api.queries as queries


@api_view(["GET"])
def twitter_tweets(request, limit):
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_tweets(int(limit) if limit.isdigit() else None)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


def twitter_tweets_export(request):
	return None


def twitter_tweets_stats(request):
	return None


def twitter_tweet(request, id):
	return None


def twitter_tweet_stats(request, id):
	return None


def twitter_tweet_replies(request, id):
	return None
