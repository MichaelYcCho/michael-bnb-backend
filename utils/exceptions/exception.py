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

    class InvalidCheckIn(APIException):
        error_code = 300003
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "오늘 보다 이전 날짜로 체크인 할수 없습니다"

    class InvalidCheckOut(APIException):
        error_code = 300004
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "체크 아웃날짜는 오늘 이후로 설정되어야합니다"

    class InvalidCheckDate(APIException):
        error_code = 300005
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "체크아웃 날짜는 체크인 날짜보다 이후여야 합니다"

    class AlreadyBooked(APIException):
        error_code = 300006
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "이미 예약된 날짜입니다"
