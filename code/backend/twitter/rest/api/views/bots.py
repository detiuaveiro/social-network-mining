from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from api import queries
from api.views.utils import create_response


def twitter_create(request):
	return None


def twitter_stats(request):
	return None

@api_view(["GET"])
def twitter_bots(request):
	"""
	Returns all the bots info
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

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


def twitter_bot(request, id):
	return None


def twitter_bot_logs(request, id):
	return None


def twitter_bot_messages(request, id):
	return None
