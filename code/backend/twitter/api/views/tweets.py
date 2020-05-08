from rest_framework.decorators import api_view
from rest_framework.status import *

from api.views.utils import create_response
import api.queries as queries


@api_view(["GET"])
def twitter_tweets(_, entries_per_page=None, page=None):
	"""

	Args:
		_:  Http Request (ignored in this function)
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: All tweets saved on databases wrapped on response's object

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

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_tweets_stats(_, entries_per_page=None, page=None):
	"""

	Args:
		_: Http Request (ignored in this function)
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: All tweets stats saved on databases wrapped on response's object

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

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_tweet(_, tweet_id):
	"""

	Args:
		_: Http Request (ignored in this function)
		tweet_id: Tweet's ID


	Returns: Tweet info wrapped  on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_tweet(int(tweet_id))
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_tweet_stats(_, tweet_id, entries_per_page=None, page=None):
	"""

	Args:
		_: Http Request (ignored in this function)
		tweet_id: Tweets's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: Tweet's stats wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_tweet_stats(int(tweet_id), entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_tweet_replies(_, tweet_id):
	"""

	Args:
		_: Http Request (ignored in this function)
		tweet_id: Tweet's ID

	Returns: Tweet's replies wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_tweet_replies(int(tweet_id))
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_search_tweets(_, tweet):
	"""

	Args:
		_:  Http Request (ignored in this function)
		tweet: Tweet to be searched

	Returns: Tweets  that matches keywords wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_search_tweets(tweet)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)