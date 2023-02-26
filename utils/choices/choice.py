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


class GenderChoices(models.TextChoices):
    MALE = ("male", "Male")
    FEMALE = ("female", "Female")


class LanguageChoices(models.TextChoices):
    KR = ("kr", "Korean")
    EN = ("en", "English")


class CurrencyChoices(models.TextChoices):
    WON = "won", "Korean Won"
    USD = "usd", "Dollar"
