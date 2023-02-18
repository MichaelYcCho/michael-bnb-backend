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

    class NotMatchingUser(APIException):
        error_code = 300001
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "예약자와 일치하지 않습니다"

    class InvalidCheckDate(APIException):
        error_code = 300002
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "체크인/체크아웃 날짜를 확인해주세요"
