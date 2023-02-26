from rest_framework import serializers

from utils.serializers import inline_serializer


class ReviewListOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = inline_serializer(
        fields={
            "id": serializers.IntegerField(),
            "avatar": serializers.URLField(),
            "username": serializers.CharField(),
        }
    )
    content = serializers.CharField(label="리뷰 내용")
    rating = serializers.IntegerField(label="평점")
