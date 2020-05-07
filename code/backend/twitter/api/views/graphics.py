from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from api import queries
from api.views.utils import create_response


@api_view(["GET"])
def entities_counter(_, ):
	"""
	Args:
		_: Http Request (ignored in this function)

	Returns: Entities counter (bots,users,tweets) info saved on database wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.entities_counter()
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def latest_tweets(_, counter, entries_per_page=None, page=None):
	"""
	Args:
		_: Http Request (ignored in this function)
		counter: Number of tweets to return
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: Latest tweets wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.latest_tweets(int(counter), entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def latest_activities_daily(_, entries_per_page=None, page=None):
	"""

	Args:
		_: Http Request (ignored in this function)
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: All bots's daily activities wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.latest_activities_daily(entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def latest_activities(_, counter, entries_per_page=None, page=None):
	"""

	Args:
		_: Http Request (ignored in this function)
		counter: Number of tweets to return
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: All bots's activities limited by counter wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.latest_activities(int(counter), entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)

@api_view(["GET"])
def stats_grouped(_, group_type):
	"""
	Args:
		_:  Http Request (ignored in this function)
		user_id: User's ID
		group_type: Keyword defining group label (day,month,year)

	Returns: Activities grouped by (day or month or year) wrapped on response's object

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

	success, data, message = queries.stats_grouped(types[:index_per_type[group_type] + 1])
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)
