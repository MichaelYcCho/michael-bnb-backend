from django.db import models


class BookingKindChoices(models.TextChoices):
    ROOM = "room", "Room"
    EXPERIENCE = "experience", "Experience"
