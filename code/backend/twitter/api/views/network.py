from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.decorators import api_view
from api.views.utils import create_response
from api import queries


@api_view(["GET"])
def twitter_network(_):
    error_messages = []
    success_messages = []
    status = HTTP_200_OK
    data = []

    success, data, message = queries.twitter_network()
    print(data)
    if success:
        success_messages.append(message)
    else:
        error_messages.append(message)
        status = HTTP_403_FORBIDDEN

    return create_response(data=data, error_messages=error_messages,
                           success_messages=success_messages, status=status)


def twitter_network_export(request):
    return None
