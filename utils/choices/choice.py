from django.db import models


class BookingKindChoices(models.TextChoices):
    ROOM = "room", "Room"
    EXPERIENCE = "experience", "Experience"


class CategoryKindChoices(models.TextChoices):
    ROOMS = "rooms", "Rooms"
    EXPERIENCES = "experiences", "Experiences"


class RoomKindChoices(models.TextChoices):
    ENTIRE_PLACE = ("entire_place", "Entire Place")
    PRIVATE_ROOM = ("private_room", "Private Room")
    SHARED_ROOM = "shared_room", "Shared Room"
