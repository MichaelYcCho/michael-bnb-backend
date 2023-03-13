from rest_framework import serializers

from categories.schemas.category import CategoryListResponse
from utils.pydantic import PydanticModelSerializer


class CategoryListOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    kind = serializers.CharField()


class CategoryListResponseSerializer(PydanticModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    kind = serializers.CharField()

    def get_py_model(self):
        return CategoryListResponse
