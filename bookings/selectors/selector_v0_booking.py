from rest_framework.request import Request

from bookings.models import Booking
from rooms.models import Room
from users.models import User


class BookingSelector:
    def __init__(self):
        pass

    @staticmethod
    def get_my_bookings_selector(user: User) -> Booking:
        """내 예약 조회"""
        return Booking.objects.filter(user=user)

    @staticmethod
    def is_exists(room: Room, request: Request) -> bool:
        """예약이 존재하는지 확인"""
        room = room
        check_in = request.query_params.get("check_in")
        check_out = request.query_params.get("check_out")

        is_allow = True

        exists = Booking.objects.filter(
            room=room,
            check_in__lte=check_out,
            check_out__gte=check_in,
        ).exists()

        if exists:
            is_allow = False

        return is_allow
