from rest_framework import serializers

from utils.serializers import inline_serializer


class CreateBookingInputSerializer(serializers.Serializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    guests = serializers.IntegerField(required=False, default=1)


class CreateBookingOutputSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    experience_time = serializers.DateTimeField()
    guests = serializers.IntegerField()


class MyBookingOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    room = inline_serializer(
        fields={
            "name": serializers.CharField(
                label="방 이름",
            ),
            "price": serializers.IntegerField(
                label="가격",
            ),
        },
    )
    kind = serializers.CharField()
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    guests = serializers.IntegerField()
    is_canceled = serializers.BooleanField()
