from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from api import queries
from api.views.utils import create_response


def twitter_create(request):
    return None


@api_view(["GET"])
def twitter_stats(_):
    """
    Get both users and twitter tweets status saved on postgres
    :return: response object
    """
    error_messages = []
    success_messages = []
    status = HTTP_200_OK
    data = []

    users_stats_success, users_stats_data, users_stats_message = queries.twitter_users_stats()

    tweets_stats_success, tweets_stats_data, tweets_stats_message = queries.twitter_tweets_stats()

    if users_stats_success and tweets_stats_success:
        success_messages.append(users_stats_message)
        success_messages.append(tweets_stats_message)
        data = users_stats_data + tweets_stats_data
    else:
        error_messages.append("Erro ao obter todas as estatisticas")
        status = HTTP_403_FORBIDDEN

    return create_response(data=data, error_messages=error_messages,
                           success_messages=success_messages, status=status)


def twitter_bots(request):
    return None

@api_view(["GET"])
def twitter_bot(_, id):
	"""
	Returns a info associated to a bot saved on neo4j
	:param id: bot's id
	:return: response Object
	"""
	error_messages = []
	success_messages = []
	status = HTTP_200_OK

	success, data, message = queries.twitter_bot(int(id))
	if success:
		success_messages.append(message)
	else:
		error_messages.append(message)
		status = HTTP_403_FORBIDDEN

	return create_response(data=data, error_messages=error_messages,
						   success_messages=success_messages, status=status)


def twitter_bot_logs(request, id):
    return None


@api_view(["GET"])
def twitter_bot_messages(_, id):
    """
    Return all privates messages from a bot
    :param id: bot's id
    :return: response object
    """
    error_messages = []
    success_messages = []
    status = HTTP_200_OK

    success, data, message = queries.twitter_bot_messages(id)
    if success:
        success_messages.append(message)
    else:
        error_messages.append(message)
        status = HTTP_403_FORBIDDEN

    return create_response(data=data, error_messages=error_messages,
                           success_messages=success_messages, status=status)
