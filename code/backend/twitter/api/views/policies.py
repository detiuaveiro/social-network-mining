from rest_framework.decorators import api_view
from api.views.utils import create_response
from rest_framework.status import *
import api.queries as queries


@api_view(["GET"])
def policies(_, entries_per_page=None, page=None):
	"""
	Return all saved policies
	:return: Response Object
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

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["GET"])
def policy(_, id):
	"""
	Return a policy specified by ID
	:param id: policy id
	:return: Response Object
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.policy(id)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["GET"])
def bot_policies(_, id, entries_per_page=None, page=None):
	"""
	Get policies by bot's id
	:param id:  bot's id
	:return: response object
	"""

	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.bot_policies(id, entries_per_page, page)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["POST"])
def add_policy(request):
	"""
	Add a new policy
	:param request:  request object
	:return: response object
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

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["DELETE"])
def remove_policy(_, id):
	"""
	Remove a policy specified by ID
	:param id: policy id
	:return: response object
	"""

	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.remove_policy(id)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["PUT"])
def update_policy(request, id):
	"""
	Update a policy specified by ID
	:param request: request object
	:param id: policy id
	:return: response object
	"""

	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.update_policy(request.data, id)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["GET"])
def instagram_policies(_):
	"""
	Return all instagram policies
	:return: response object
	"""

	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.policy_by_service("Instagram")
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


@api_view(["GET"])
def twitter_policies(_):
	"""
	Return all twitter policies
	:return: response object
	"""

	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.policy_by_service("Twitter")
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)
