from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.decorators import api_view
from api.views.utils import create_response, cypher_query_generator
from api import queries
from django.views.decorators.cache import cache_page
from rest.settings import CACHE_TTL


@cache_page(CACHE_TTL)
@api_view(["GET"])
def twitter_network(_):
	"""

	Args:
		_: Http Request (ignored in this function)

	Returns:  Neo4'j network in json format wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_network()

	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)


@cache_page(CACHE_TTL)
@api_view(["GET"])
def twitter_sub_network(request):
	"""

	Args:
		request:  Http Request

	Returns: Neo4'j sub network in json format wrapped on response's object

	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	try:
		success, data, message = queries.twitter_sub_network(request.data)
		if success:
			success_messages.append(message)
		else:
			error_messages.append(message)
			status = HTTP_403_FORBIDDEN
	except Exception as e:
		status = HTTP_403_FORBIDDEN
		error_messages.append(str(e))

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)
