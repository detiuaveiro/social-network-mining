from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


def create_response(data=None, success_messages=None, error_messages=None, status=HTTP_200_OK):
    return Response({
        "data": data,
        "success_messages": success_messages,
        "error_messages": error_messages,
    }, status=status)
