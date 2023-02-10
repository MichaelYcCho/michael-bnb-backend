from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User


class SignUpInputSerializer(serializers.Serializer):
    """
    Input Serializer
    """

    username = serializers.CharField()
    name = serializers.CharField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()

    class Meta:
        ref_name = "sign_up_input"


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
