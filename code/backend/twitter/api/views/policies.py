from rest_framework.decorators import api_view
from api.views.utils import create_response
from rest_framework.status import *
import api.queries as queries


@api_view(["GET"])
def policies(_, entries_per_page=None, page=None):
	"""

	Args:
		_:  Http Request (ignored in this function)
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: All policies saved wrapped on response's object

	"""

	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.policies(entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def policy(_, policy_id):
	"""

	Args:
		_: Http Request (ignored in this function)
		policy_id: Policy's ID

	Returns: Policy's info wrapped on  response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.policy(int(policy_id))
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def bot_policies(_, bot_id, entries_per_page=None, page=None):
	"""
	
	Args:
		_:  Http Request (ignored in this function)
		bot_id: Bot's ID
		entries_per_page: Number of entries per page or None
		page: Number of page the user wants to retrieve or None

	Returns: Bot assigned policies wrapped on response's object

	"""

	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.bot_policies(int(bot_id), entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["GET"])
def get_number_policies(_):
	"""
	Args:
		_: HTTP Request (ignored in this function)

	Returns: Total number of policies in the database
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.get_number_policies()
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["POST"])
def add_policy(request):
	"""

	Args:
		request: Http Request

	Returns: Add operation status wrapped on response's object

	"""

	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.add_policy(request.data)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["DELETE"])
def remove_policy(_, policy_id):
	"""

	Args:
		_:
		policy_id: Policy's ID

	Returns: Remove operation status wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.remove_policy(int(policy_id))
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["PUT"])
def update_policy(request, policy_id):
	"""

	Args:
		request: Http Request
		policy_id: Policy'ID

	Returns: Update operation status wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.update_policy(request.data, int(policy_id))
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@api_view(["POST"])
def add_emails(request):
	"""
	Args:
		request: Http Request (ignored in this function)

	Returns: Add operation status wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, message = queries.add_emails(request.data)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(error_messages=error_messages, success_messages=success_messages, status=status)
