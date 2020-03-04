from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from api import queries
from api.views.utils import create_response


@api_view(["GET"])
def twitter_users(request):
	"""
	Returns all the users saved on the mongo database
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_users()
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


def twitter_users_stats(request):
	return None


@api_view(["GET"])
def twitter_user(request, id):
	"""
	Returns the user with the requested id

	Keyword arguments:
	id: id of the user wanted
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_user(int(id))
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


def twitter_user_tweets(request, id):
	return None


def twitter_user_followers(request, id):
	return None


def twitter_user_following(request, id):
	return None


def twitter_user_stats(request, id):
	return None


def twitter_users_export(request):
	return None
