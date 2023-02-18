from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.exceptions import APIException


class BaseExceptions:
    pass


class RoomExceptions:
    pass


class BookingExceptions:
    class NotFoundBooking(APIException):
        error_code = 300000
        status_code = status.HTTP_404_NOT_FOUND
        default_detail = "예약 내역이 존재하지 않습니다"
