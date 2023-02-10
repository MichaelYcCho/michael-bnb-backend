from rest_framework import serializers


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
