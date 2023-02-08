from rest_framework.exceptions import NotFound

from rooms.models import Room


class RoomSelector:
    def __init__(self, room_pk: int):
        self.room_pk = room_pk

    def get_room(self) -> Room:
        room = Room.objects.filter(pk=self.room_pk).first()
        if room is None:
            raise NotFound
        return room
