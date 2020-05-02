from rest_framework.decorators import api_view
from rest_framework.status import *

from api.views.utils import create_response
import api.queries as queries


@api_view(["GET"])
def twitter_tweets(request, entries_per_page=None, page=None):
	"""Function to return all tweets within a given limit (if no limit is given, it returns all saved tweets)
	:param limit: defines how many tweets to return
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_tweets(entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
	                       success_messages=success_messages, status=status)


def twitter_tweets_export(request):
	return None


@api_view(["GET"])
def twitter_tweets_stats(request, entries_per_page=None, page=None):
	"""Function to obtain all the tweets stats saved on postgres
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_tweets_stats(entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
	                       success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_tweet(request, id):
	"""Returns a list of all tweets with the given id
	:param id: tweet id (in terms of the Tweet objects saved on the mongo db, it corresponds to str_id)
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_tweet(id)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
	                       success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_tweet_stats(request, id, entries_per_page=None, page=None):
	"""Function to obtain the stats of a determined tweet
	:param id: id of the tweet whom we want the stats
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_tweet_stats(id, entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
	                       success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_tweet_replies(request,id):
    """Returns a list of all tweets which are replies to the tweet with the given id
    :param id: tweet id in relation to which we want the replies
    """
    error_messages = []
    success_messages = []
    status = HTTP_200_OK

    success, data, message = queries.twitter_tweet_replies(id)
    if success:
        success_messages.append(message)
    else:
        error_messages.append(message)
        status = HTTP_403_FORBIDDEN

    return create_response(data=data, error_messages=error_messages,
                           success_messages=success_messages, status=status)
