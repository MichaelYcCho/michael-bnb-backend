from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from bookings.models import Booking
from bookings.selectors.selector_v1_booking import BookingSelector
from bookings.serializers import (
    CreateBookingInputSerializer,
    CreateBookingOutputSerializer,
    MyBookingOutputSerializer,
    ManageBookingsOutPutSerializer,
)
from bookings.services.service_v1_booking import (
    BookingCreateService,
    BookingCancelService,
)
from rooms.models import Room
from rooms.selectors.selector_v0_room import RoomSelector


class GetMyBookingsAPI(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="V1 나의 예약조회 API",
        operation_description="내 예약정보를 조회한다(Guest)",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                "조회 완료", MyBookingOutputSerializer(many=True)
            ),
        },
    )
    def get(self, request: Request) -> Response:
        selector = BookingSelector()
        bookings = selector.get_my_bookings_selector(request.user)
        serializer = MyBookingOutputSerializer(bookings, many=True)
        return Response(serializer.data)


class ManageBookingsAPI(APIView):

    # TODO : Host Permission
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="V1 나의 Booking 관리 API",
        operation_description="내 방의 예약정보를 조회한다(Host)",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                "조회 완료", MyBookingOutputSerializer(many=True)
            ),
        },
    )
    def get(self, request: Request) -> Response:
        rooms = Room.objects.filter(owner=request.user)
        bookings = Booking.objects.filter(room__in=rooms)
        serializer = ManageBookingsOutPutSerializer(bookings, many=True)
        return Response(serializer.data)


class CancelBookingAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, booking_id: int) -> Response:
        selector = BookingSelector(booking_id)
        booking = selector.get_booking()

        service = BookingCancelService(request.user, booking)
        service.cancel_booking()

        return Response(status=status.HTTP_200_OK)


class CheckBookingAPI(APIView):
    def get(self, request: Request, room_id: int) -> Response:
        room_selector = RoomSelector()
        room = room_selector.get_room(room_id)
        booking_selector = BookingSelector()
        is_allow = booking_selector.is_exists(room, request)

        return Response({"is_allow": is_allow})


class CreateBookingsAPI(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, room_id: int) -> Response:
        """
        예약 생성 API
        """
        selector = RoomSelector()
        room = selector.get_room(room_id)

        input_serializer = CreateBookingInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        booking_service = BookingCreateService(
            request.user, room, input_serializer.data
        )
        booking_service.validate()
        booking = booking_service.create_booking()

        serializer = CreateBookingOutputSerializer(booking)
        return Response(serializer.data)
