from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.views import APIView

from rest_framework.response import Response
from bookings.models import Booking
from bookings.serializers import (
    CreateBookingInputSerializer,
    CreateBookingOutputSerializer,
)
from bookings.services.service_v0_booking import BookingService
from rooms.selectors.selector_v0_room import RoomSelector


class RoomBookingCheck(APIView):
    def get(self, request: Request, room_pk: int) -> Response:
        selector = RoomSelector(room_pk)
        room = selector.get_room()
        check_in = request.query_params.get("check_in")
        check_out = request.query_params.get("check_out")

        exists = Booking.objects.filter(
            room=room,
            check_in__lte=check_out,
            check_out__gte=check_in,
        ).exists()
        if exists:
            return Response({"ok": False})
        return Response({"ok": True})


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, room_pk: int) -> Response:
        """
        예약 생성 API
        """
        selector = RoomSelector(room_pk)
        room = selector.get_room()

        input_serializer = CreateBookingInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        booking_service = BookingService(request.user, room, input_serializer.data)
        booking_service.validate()
        booking = booking_service.create_booking()

        serializer = CreateBookingOutputSerializer(booking)
        return Response(serializer.data)
