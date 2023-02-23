from rest_framework import serializers

from utils.serializers import inline_serializer
from rooms.models import Amenity, Room
from medias.serializers import PhotoSerializer


class RoomCreateInputSerializer(serializers.Serializer):
    """
    Room Create Input Serializer
    """

    name = serializers.CharField(label="방 이름")
    country = serializers.CharField(label="국가")
    city = serializers.CharField(label="도시")
    address = serializers.CharField(label="주소")
    kind = serializers.CharField(label="방 종류")
    price = serializers.IntegerField(label="가격", default=0)
    rooms = serializers.IntegerField(label="방 개수", default=1)
    toilets = serializers.IntegerField(label="화장실 개수", default=1)
    description = serializers.CharField(label="방 설명")
    pet_friendly = serializers.BooleanField(label="반려동물 동반 가능 여부", default=False)
    category = serializers.CharField(label="카테고리 ID")
    amenities = serializers.ListField(child=serializers.CharField(), allow_null=True)

    class Meta:
        ref_name = "room_create_input"


class RoomCreateOutputSerializer(serializers.Serializer):
    """
    Room Create Output Serializer
    """

    id = serializers.IntegerField()

    class Meta:
        ref_name = "room_create_output"


class RoomListOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    owner = inline_serializer(
        fields={
            "id": serializers.IntegerField(),
            "username": serializers.CharField(),
        }
    )
    name = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    price = serializers.IntegerField()
    rating = serializers.FloatField(source="_rating")
    is_owner = serializers.BooleanField(source="_is_owner")
    photos = inline_serializer(
        many=True,  # type:ignore
        fields={
            "id": serializers.IntegerField(required=False),
            "file": serializers.URLField(required=False),
            "description": serializers.CharField(required=False),
        },
    )
    is_wish_listed = serializers.BooleanField(source="_is_wish_listed")


class RoomDetailOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    price = serializers.IntegerField()
    toilets = serializers.IntegerField()
    rooms = serializers.IntegerField()
    address = serializers.CharField()
    pet_friendly = serializers.BooleanField()
    kind = serializers.CharField()
    description = serializers.CharField()
    owner = inline_serializer(
        fields={
            "id": serializers.IntegerField(),
            "username": serializers.CharField(),
            "avatar": serializers.URLField(),
        }
    )
    amenities = inline_serializer(
        many=True,  # type:ignore
        fields={
            "id": serializers.IntegerField(),
            "name": serializers.CharField(),
            "description": serializers.CharField(),
        },
    )
    category = inline_serializer(
        fields={
            "id": serializers.IntegerField(),
            "name": serializers.CharField(),
            "kind": serializers.CharField(),
        }
    )
    rating = serializers.FloatField(source="_rating")
    is_owner = serializers.BooleanField(source="_is_owner")
    photos = inline_serializer(
        many=True,  # type:ignore
        fields={
            "id": serializers.IntegerField(required=False),
            "file": serializers.URLField(required=False),
            "description": serializers.CharField(required=False),
        },
    )


class RoomUpdateInputSerializer(serializers.Serializer):
    """
    Room Update Input Serializer
    """

    room_id = serializers.IntegerField(label="방 ID")
    name = serializers.CharField(label="방 이름")
    country = serializers.CharField(label="국가")
    city = serializers.CharField(label="도시")
    address = serializers.CharField(label="주소")
    price = serializers.IntegerField(label="가격")
    rooms = serializers.IntegerField(label="방 개수")
    toilets = serializers.IntegerField(label="화장실 개수")
    description = serializers.CharField(label="방 설명", allow_blank=True)
    pet_friendly = serializers.BooleanField(label="반려동물 동반 가능 여부", default=False)
    category = serializers.CharField(label="카테고리 ID")
    kind = serializers.CharField(label="방 종류")
    amenities = serializers.ListField(child=serializers.CharField(), allow_null=True)

    class Meta:
        ref_name = "room_create_input"


class AmenityListInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        ref_name = "amenity_list_input"


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "pk",
            "name",
            "description",
        )


class RoomListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "owner",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
