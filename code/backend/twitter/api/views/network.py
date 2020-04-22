from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from api import queries
from api.views.utils import create_response, cypher_query_generator


def twitter_network(request):
    return None


def twitter_network_export(request):
    return None


@api_view(["GET"])
def twitter_sub_network(request):
    error_messages = []
    success_messages = []
    status = HTTP_200_OK
    data = []

    try:
        success, data, message = queries.twitter_sub_network(cypher_query_generator(request.GET))
        if success:
            success_messages.append(message)
        else:
            error_messages.append(message)
            status = HTTP_403_FORBIDDEN
    except Exception as e:
        status = HTTP_403_FORBIDDEN
        error_messages.append(str(e))

    return create_response(data=data, error_messages=error_messages,
                           success_messages=success_messages, status=status)
