import random
from typing import Type, Optional

from django.db.models import Model
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

HTTP_404_RESPONSE = Response(status=status.HTTP_404_NOT_FOUND)


def get_object_by_pk(model: Type[Model], pk) -> Optional[Type[Model]]:
    try:
        obj = model.objects.get(pk=pk)
        return obj
    except model.DoesNotExist:
        return None


def get_object_or_404_response(model: Type[Model], serializer: Type[serializers.ModelSerializer], *,
                               pk):
    obj = get_object_by_pk(model, pk=pk)
    if obj is None:
        return HTTP_404_RESPONSE
    data = serializer(obj).data
    return Response(data)


def get_list_or_404_response(model: Type[Model], serializer: Type[serializers.ModelSerializer]):
    objs = model.objects.all()
    if not objs:
        return HTTP_404_RESPONSE
    data = serializer(objs, many=True).data
    return Response(data)


def random_entity(cls: Type[Model]) -> Type[Model]:
    return cls.objects.get(pk=random.randint(0, cls.objects.count()))
