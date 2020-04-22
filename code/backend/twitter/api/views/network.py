from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.decorators import api_view
from api.views.utils import create_response, cypher_query_generator
from api import queries


@api_view(["GET"])
def twitter_network(_):
    error_messages = []
    success_messages = []
    status = HTTP_200_OK

    success, data, message = queries.twitter_network()

    if success:
        success_messages.append(message)
    else:
        error_messages.append(message)
        status = HTTP_403_FORBIDDEN

    return create_response(data=data, error_messages=error_messages,
                           success_messages=success_messages, status=status)


def twitter_network_export(request):
    return None


@api_view(["GET"])
def twitter_sub_network(request):
    """
    Get sub network
    Args:
        request: http request object

    Returns:

    """
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
