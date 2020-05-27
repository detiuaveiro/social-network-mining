from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from api import queries

from api.views.utils import create_response


@api_view(["GET"])
def twitter_users_count(_):
	"""
	Args:
		_:  Http Request (ignored in this function)
	Returns: Number of  users saved on the mongo database wrapped on response's object
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_users_count()
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_users(_, protected, entries_per_page=None, page=None):
	"""
	Args:
		protected:  Boolean to identify a protected user
		_:  Http Request (ignored in this function)
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None
	Returns: Users saved on the mongo database wrapped on response's object
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_users(entries_per_page, page, protected == 'T')
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_users_stats(_, protected, entries_per_page=None, page=None):
	"""
	Args:
		protected:  Boolean to identify a protected user
		_: Http Request (ignored in this function)
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: Stats saved on the postgres database wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_users_stats(entries_per_page, page, protected == 'T')
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user(_, user_id):
	"""

	Args:
		_: Http Request (ignored in this function)
		user_id: User's ID

	Returns: User info defined by user_id parameter wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_user(user_id)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user_tweets(_, user_id, entries_per_page=None, page=None):
	"""

	Args:
		_: Http Request (ignored in this function)
		user_id: User's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: User's tweets wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_user_tweets(user_id, entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user_followers(_, user_id, entries_per_page=None, page=None):
	"""

	Args:
		_: Http Request (ignored in this function)
		user_id: User's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: User's followers wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_user_followers(user_id, entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user_following(_, user_id, entries_per_page=None, page=None):
	"""

	Args:
		_: Http Request (ignored in this function)
		user_id: User's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: User's following wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_user_following(user_id, entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user_stats(_, user_id, entries_per_page=None, page=None):
	"""

	Args:
		_: Http Request (ignored in this function)
		user_id: User's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: User's stats wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_user_stats(int(user_id), entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_search_users(_, keywords, protected, entries_per_page=None, page=None):
	"""

	Args:
		_:  Http Request (ignored in this function)
		keywords: Words to be searched
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: User's  that matches keywords wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_search_users(keywords, protected == 'T', entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_search_users_strict(_, keyword, type):
	"""

	Args:
		_:  Http Request (ignored in this function)
		keyword: Word to be searched
		type: Type of User to be searched (Bot or User)

	Returns: Users that match keyword wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_search_users_strict(keyword, type)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_user_stats_grouped(_, user_id, group_type):
	"""
	Args:
		_:  Http Request (ignored in this function)
		user_id: User's ID
		group_type: Keyword defining group label (day,month,year)

	Returns: User's stats  grouped by (day or month or year) wrapped on response's object

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

	success, data, message = queries.twitter_user_stats_grouped(user_id, types[:index_per_type[group_type] + 1])
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_users_type(_, user_id):
	"""

	Args:
		_: Http Request (ignored in this function)
		user_id: User's ID

	Returns: User's type wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_users_type(user_id)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_strict_search(_, keyword):
	"""
	Args:
		_: Http Request (ignored in this function)
		keyword: Keyword to get from twitter

	Returns: Matches for the keyword
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_strict_search(keyword)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)
