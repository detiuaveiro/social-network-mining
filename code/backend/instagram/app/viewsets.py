from django.utils.html import escape as html_escape
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

import app.serializers as serializers
from app.models import Image
from app.utils import random_entity, HTTP_404_RESPONSE, get_object_by_pk


class RetrieveEntityMixin:
    def retrieve(self, request, pk=None):
        obj = get_object_by_pk(self.model, pk=pk)
        if obj is None:
            return HTTP_404_RESPONSE
        data = self.serializer_class(obj).data
        return Response(data)


class RandomEntityMixin:
    @action(detail=False, methods=["get"])
    def random(self, request, *args, **kwargs):
        try:
            obj = random_entity(self.model)
            data = self.serializer_class(obj).data
            return Response(data)
        except self.model.DoesNotExist:
            return HTTP_404_RESPONSE


class ImageViewSet(viewsets.ViewSet, RandomEntityMixin):
    model = Image
    serializer_class = serializers.ImageSerializer

    @action(detail=False, methods=['get'])
    def search(self, request, *args, **kwags):
        clean_parameters = {k: html_escape(v) for k, v in request.GET.items()}
        short_code = clean_parameters.get("short_code", None)
        if short_code is None:
            return HTTP_404_RESPONSE
        try:
            serializers.ImagePostSerializer({'short_code' : short_code, })
            obj = self.model.objects.get(short_code=short_code)
            return Response(self.serializer_class(obj).data)
        except self.model.DoesNotExist:
            return HTTP_404_RESPONSE

    def create(self, request, format=None):
        image_file = request.FILES.get("file", None)
        if image_file is None:
            return Response("No file provided!", status=status.HTTP_400_BAD_REQUEST)
        date, short_code = image_file.name.split("__")
        obj, created = self.model.objects.get_or_create(short_code=short_code, file=image_file)
        if created:
            return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)
        else:
            return Response("File already created!", status=status.HTTP_400_BAD_REQUEST)

