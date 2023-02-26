from django.db import transaction
from rest_framework.request import Request

from medias.models.photo import Photo
from rooms.models.room import Room


class PhotoService:
    def __init__(self, request: Request, data: dict) -> None:
        self.request = request
        self.id = data.get("id")
        self.file = data.get("file")
        self.description = data.get("description")

    def create_photo(self, room: Room) -> Photo:
        with transaction.atomic():
            photo = Photo(
                file=self.file,
                description=self.description,
            )
            photo.room = room
            photo.full_clean()
            photo.save()
            return photo
