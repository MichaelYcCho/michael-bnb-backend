from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from rest_framework.response import Response
from bookings.selectors.selector_v0_booking import BookingSelector
from bookings.serializers import (
    CreateBookingInputSerializer,
    CreateBookingOutputSerializer,
    MyBookingOutputSerializer,
)
from bookings.services.service_v0_booking import (
    BookingCreateService,
    BookingCancelService,
)
from rooms.selectors.selector_v0_room import RoomSelector


class GetMyBookingsAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        selector = BookingSelector()
        bookings = selector.get_my_bookings_selector(request.user)
        serializer = MyBookingOutputSerializer(bookings, many=True)
        return Response(serializer.data)


class CancelBookingAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id: int):
        selector = BookingSelector(booking_id)
        booking = selector.get_booking()

        service = BookingCancelService(request.user, booking)
        service.cancel_booking()

        return Response(status=status.HTTP_200_OK)


class CheckBookingAPI(APIView):
    def get(self, request: Request, room_pk: int) -> Response:
        room_selector = RoomSelector(room_pk)
        room = room_selector.get_room()
        booking_selector = BookingSelector()
        is_allow = booking_selector.is_exists(room, request)

        return Response({"is_allow": is_allow})


class CreateBookingsAPI(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, room_pk: int) -> Response:
        """
        예약 생성 API
        """
        selector = RoomSelector(room_pk)
        room = selector.get_room()

        input_serializer = CreateBookingInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        booking_service = BookingCreateService(
            request.user, room, input_serializer.data
        )
        booking_service.validate()
        booking = booking_service.create_booking()

        serializer = CreateBookingOutputSerializer(booking)
        return Response(serializer.data)
