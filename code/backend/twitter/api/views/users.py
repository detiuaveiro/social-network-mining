from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from api import queries
from api.views.utils import create_response


@api_view(["GET"])
def twitter_users(request, entries_per_page=None, page=None):
	"""Returns all the users saved on the mongo database
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_users(entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_users_stats(request, entries_per_page=None, page=None):
	"""Get all users status saved on postgres
"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_users_stats(entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user(request, id):
	"""Returns the user with the requested id
	:param id: id of the user wanted
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


@api_view(["GET"])
def twitter_user_tweets(request, id, entries_per_page=None, page=None):
	"""Returns the tweets of the user with the requested id
	:param id: id of the user in relation which we want his tweets
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_user_tweets(int(id), entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user_followers(request, id):
	"""Function to retrieve all the followers of some requested user
	:param id: id of the user whom we want the followers
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_user_followers(int(id))
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user_following(request, id):
	"""Function to retrieve all the following users of some requested user
	:param id: id of the user whom we want the following users
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_user_following(int(id))
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user_stats(request, id, entries_per_page=None, page=None):
	"""Function to get all stats of a requested user
:param id: user's id whom we want the stats
"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_user_stats(int(id), entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user_stats_grouped(_, id, type):
	"""Function to get all stats grouped
		:param id: user's id whom we want the stats
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	index_per_type = {
		'year': 0,
		'month': 1,
		'day': 2
	}
	types = ["year", "month", "day"]
	
	success, data, message = queries.twitter_user_stats_grouped(int(id), types[:index_per_type[type] + 1])
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


def twitter_users_export(request):
	return None
