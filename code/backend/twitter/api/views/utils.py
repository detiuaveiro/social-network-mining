from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


def create_response(data=None, success_messages=None, error_messages=None, status=HTTP_200_OK):
    return Response({
        "data": data,
        "success_messages": success_messages,
        "error_messages": error_messages,
    }, status=status)


def cypher_query_generator(request_params):
    bots = request_params.getlist('bots_id', [])
    users = [int(i) for i in request_params.getlist('users_id', [])]

    queries = []
    for bot_id in bots:

        query = f"match result=(entity1 {{ id : {bot_id} }})-[:FOLLOWS]->(entity2) return result"
        queries.append(("bots", bot_id, query))

    return queries
