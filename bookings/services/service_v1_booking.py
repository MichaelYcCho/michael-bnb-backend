from datetime import date, datetime

from django.utils import timezone
from rest_framework import serializers

from bookings.models import Booking
from rooms.models import Room
from users.models import User
from utils.choices import BookingKindChoices
from utils.exceptions.exception import BookingExceptions


class BookingCreateService:
    def __init__(self, user: User, room: Room, serializer_data: dict):
        self.user = user
        self.room = room
        self.now = timezone.localtime(timezone.now()).date()
        self.check_in = datetime.strptime(
            serializer_data["check_in"], "%Y-%m-%d"
        ).date()
        self.check_out = datetime.strptime(
            serializer_data["check_out"], "%Y-%m-%d"
        ).date()
        self.guests = serializer_data["guests"]

    def validate_check_in(self, check_in: date):
        if self.now > check_in:
            raise BookingExceptions.InvalidCheckIn
        return check_in

    def validate_check_out(self, check_out: date):
        if self.now > check_out:
            raise BookingExceptions.InvalidCheckOut
        return check_out

    def validate(self) -> bool:
        self.validate_check_in(self.check_in)
        self.validate_check_out(self.check_out)

        room = self.room
        if self.check_out <= self.check_in:
            raise BookingExceptions.InvalidCheckDate

        if Booking.objects.filter(
            room=room,
            check_in__lte=self.check_out,
            check_out__gte=self.check_in,
            is_canceled=False,
        ).exists():
            raise BookingExceptions.AlreadyBooked
        return True

    def create_booking(self) -> Booking:
        self.validate()
        booking = Booking(
            room=self.room,
            user=self.user,
            kind=BookingKindChoices.ROOM,
            check_in=self.check_in,
            check_out=self.check_out,
            guests=self.guests,
        )
        booking.full_clean()
        booking.save()

        return booking


class BookingCancelService:
    def __init__(self, user: User, booking: Booking) -> None:
        self.user = user
        self.booking = booking

    def cancel_booking(self) -> None:
        self.booking.is_canceled = True
        self.booking.save()
