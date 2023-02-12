from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from rooms.models import Room


class RoomSelector:
    def __init__(self, request: Request = None):
        self.request = request

    @staticmethod
    def get_room_avg_rating(room_id: int) -> float:
        room = Room.objects.filter(pk=room_id).first()

        if room is None:
            raise NotFound

        total_rating = 0
        count = room.reviews.count()

        if count == 0:
            return total_rating

        for reviews in room.reviews.all().values("rating"):
            total_rating += reviews.rating["rating"]
        return round(total_rating / count, 2)

    def is_owner(self, room_id: int) -> bool:
        room = Room.objects.filter(pk=room_id).first()
        if room is None:
            raise NotFound
        return room.owner == self.request.user

    def is_wish_listed(self, room_id: int) -> bool:
        room = Room.objects.filter(pk=room_id).first()
        if self.request.user.is_anonymous:
            return False

        wish_list = self.request.user.wishlists.all()

        if room is None:
            raise NotFound

        is_wish_listed = wish_list.filter(rooms__pk=room_id).exists()

        return is_wish_listed

    def get_all_rooms(self) -> Room:
        rooms = Room.objects.all()

        for room in rooms:
            room._rating = self.get_room_avg_rating(room.id)
            room._is_owner = self.is_owner(room.id)
            room._is_wish_listed = self.is_wish_listed(room.id)

        return rooms

    @staticmethod
    def get_room(room_id: int) -> Room:
        room = Room.objects.filter(pk=room_id).first()
        if room is None:
            raise NotFound
        return room
