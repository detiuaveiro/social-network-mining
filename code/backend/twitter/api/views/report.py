from rest_framework.decorators import api_view
from api.views.utils import create_response
from rest_framework.status import *
import api.queries as queries


@api_view(["POST"])
def create_report(request):
	"""
	Args:
		request: HTTP Request
	Returns: Create a new Report based on Request
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.create_report(request.data)
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages, success_messages=success_messages, status=status)
