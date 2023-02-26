from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from medias.models.photo import Photo


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
        )


class PhotoCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    file = serializers.URLField()
    description = serializers.CharField()
