from rest_framework.request import Request

from bookings.models import Booking
from rooms.models import Room
from users.models import User


class BookingSelector:
    def __init__(self, pk: int = None) -> None:
        self.booking_pk = pk

    def get_booking(self) -> Booking:
        """예약 조회"""
        booking = Booking.objects.filter(pk=self.booking_pk).first()
        if booking:
            return booking
        raise Booking.DoesNotExist

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
            is_canceled=False,
        ).exists()

        if exists:
            is_allow = False

        return is_allow
