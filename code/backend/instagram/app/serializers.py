from rest_framework import serializers

from app.models import Image


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'short_code', 'total_voted', "total_score", 'image_url')

    def get_image_url(self, obj: Image):
        return obj.file.url


class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('short_code', 'file')
