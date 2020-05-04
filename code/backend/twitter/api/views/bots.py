from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from api import queries
from api.views.utils import create_response


@api_view(["GET"])
def twitter_bots(_):
	"""

	Args:
		_: Http Request (ignored in this function)

	Returns: All bots's info saved on database wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_bots()
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_bot(_, bot_id):
	"""

	Args:
		_: Http Request (ignored in this function)
		bot_id: Bot's ID

	Returns: Bot's info wrapped on  response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_bot(bot_id)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_bot_logs(_, bot_id, entries_per_page=None, page=None):
	"""

	Args:
		_: Http Request (ignored in this function)
		bot_id: Bots's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: Bot's logs wrapped on response's object

	"""

	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_bot_logs(bot_id, entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_bot_messages(_, bot_id):
	"""

	Args:
		_: Http Request (ignored in this function)
		bot_id: Bot's ID

	Returns: Bot's direct messages wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_bot_messages(int(bot_id))
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)
