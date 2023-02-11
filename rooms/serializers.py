from rest_framework import serializers

from utils.serializers import inline_serializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist
from .selectors.selector_v0_room import RoomSelector


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "pk",
            "name",
            "description",
        )


class RoomDetailSerializer(serializers.ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        selector = RoomSelector()
        return selector.get_room_avg_rating(room.id)

    def get_is_owner(self, room):
        request = self.context.get("request")
        if request:
            return room.owner == request.user
        return False

    def get_is_liked(self, room) -> bool:
        request = self.context.get("request")
        is_liked = False

        if request.user.is_authenticated:
            is_liked = Wishlist.objects.filter(
                user=request.user,
                rooms__pk=room.pk,
            ).exists()

        return is_liked


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
