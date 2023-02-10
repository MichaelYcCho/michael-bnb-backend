from rest_framework.request import Request

from bookings.models import Booking
from rooms.models import Room


class BookingSelector:
    def __init__(self, room: Room, request: Request):
        self.room = room
        self.check_in = request.query_params.get("check_in")
        self.check_out = request.query_params.get("check_out")

    def is_exists(self) -> bool:
        """예약이 존재하는지 확인"""
        is_allow = True

        exists = Booking.objects.filter(
            room=self.room,
            check_in__lte=self.check_out,
            check_out__gte=self.check_in,
        ).exists()

        if exists:
            is_allow = False

        return is_allow
