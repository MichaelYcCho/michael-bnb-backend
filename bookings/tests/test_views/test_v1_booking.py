from datetime import datetime

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from model_mommy import mommy


class BookingTestCase(APITestCase):
    """
    Booking 조회, 삭제 테스트케이스
    """

    def setUp(self) -> None:
        self.owner = mommy.make("users.User")
        self.guest = mommy.make("users.User")
        self.nobody = mommy.make("users.User")
        self.category = mommy.make("Category", kind="rooms")
        self.amenity = mommy.make("Amenity", name="TV")
        self.room = mommy.make("Room", owner=self.owner, category=self.category)
        self.room.amenities.add(self.amenity)

        self.booking = mommy.make("Booking", room=self.room, user=self.guest)

    def test_success_get_my_booking_None(self) -> None:
        """내 예약내역 조회 -> 조회결과 없을때"""

        url = "/api/bookings/v1/my"
        self.client.force_authenticate(self.nobody)
        res = self.client.get(url)

        self.assertEqual(len(res.json()), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_success_get_managing_booking(self) -> None:
        """내 방에대한 예약내역 조회"""

        url = "/api/bookings/v1/manage"
        self.client.force_authenticate(self.owner)
        res = self.client.get(url)

        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_success_get_my_booking(self) -> None:
        """내 예약내역 조회"""

        url = "/api/bookings/v1/my"
        self.client.force_authenticate(self.guest)
        res = self.client.get(url)

        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_success_cancel_booking(self) -> None:
        """예약 취소 -> 성공"""

        url = f"/api/bookings/v1/cancel/{self.booking.id}"
        self.client.force_authenticate(self.guest)
        res = self.client.patch(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_failed_cancel_wrong_booking(self) -> None:
        """예약 취소 실패 -> 존재하지않는 예약번호"""

        url = f"/api/bookings/v1/cancel/99999"
        self.client.force_authenticate(self.guest)
        res = self.client.patch(url)

        self.assertEqual(res.json()["error_code"], 300000)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_failed_cancel_not_matching_booking_user(self) -> None:
        """예약 취소 실패 -> 예약자와 취소 요청자가 다름"""

        url = f"/api/bookings/v1/cancel/{self.booking.id}"
        self.client.force_authenticate(self.nobody)
        res = self.client.patch(url)

        self.assertEqual(res.json()["error_code"], 300001)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failed_cancel_booking(self) -> None:
        """예약 취소 실패 -> 이미 취소된 예약"""
        self.booking.is_canceled = True
        self.booking.save()

        url = f"/api/bookings/v1/cancel/{self.booking.id}"
        self.client.force_authenticate(self.nobody)
        res = self.client.patch(url)

        self.assertEqual(res.json()["error_code"], 300000)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class BookingCheckTestCase(APITestCase):
    """
    Booking 가능 날짜, 예약 생성 테스트케이스
    """

    def setUp(self) -> None:
        self.guest = mommy.make("users.User")
        self.category = mommy.make("Category", kind="rooms")
        self.owner = mommy.make("users.User")
        self.room = mommy.make("Room", owner=self.owner, category=self.category)
        self.amenity = mommy.make("Amenity", name="TV")
        self.room.amenities.add(self.amenity)

    def test_success_check_booking(self) -> None:
        """예약 존재여부 조회 성공 -> allow=True"""
        url = f"/api/bookings/v1/check/{self.room.id}?check_in=2023-02-19&check_out=2023-02-20"
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_success_check_booking_allow_false(self) -> None:
        """예약 존재여부 조회 성공 -> allow=False"""
        someone = mommy.make("users.User")

        mommy.make(
            "Booking",
            room=self.room,
            user=someone,
            check_in=datetime(2023, 2, 19),
            check_out=datetime(2023, 2, 20),
        )

        url = f"/api/bookings/v1/check/{self.room.id}?check_in=2023-02-19&check_out=2023-02-20"
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_failed_check_booking(self) -> None:
        """예약 존재여부 조회 -> 실패, 체크인/체크아웃 날짜 미기입"""

        url = f"/api/bookings/v1/check/{self.room.id}"
        res = self.client.get(url)

        self.assertEqual(res.json()["error_code"], 300005)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_create_booking(self) -> None:
        """예약 생성 성공"""
        url = "/api/bookings/v1/create"
        data = {
            "room_id": self.room.id,
            "guests": 2,
            "check_in": "2023-02-21",
            "check_out": "2023-02-25",
        }
        self.client.force_authenticate(self.guest)
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_failed_create_already_booking(self) -> None:
        """예약 생성 실패 -> 이미 예약된 방"""
        mommy.make(
            "Booking",
            room=self.room,
            user=self.guest,
            check_in=datetime(2023, 2, 21),
            check_out=datetime(2023, 2, 25),
        )

        url = "/api/bookings/v1/create"
        data = {
            "room_id": self.room.id,
            "guests": 2,
            "check_in": "2023-02-21",
            "check_out": "2023-02-25",
        }
        self.client.force_authenticate(self.guest)
        res = self.client.post(url, data)

        self.assertEqual(res.json()["error_code"], 300006)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2023-02-03", tz_offset=9)
    def test_failed_create_booking_check_in(self) -> None:
        """예약 생성 실패 -> 체크인이 오늘 이전값일때"""

        url = "/api/bookings/v1/create"
        data = {
            "room_id": self.room.id,
            "guests": 2,
            "check_in": "2023-01-21",
            "check_out": "2023-02-25",
        }
        self.client.force_authenticate(self.guest)
        res = self.client.post(url, data)

        self.assertEqual(res.json()["error_code"], 300003)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2023-02-05", tz_offset=9)
    def test_failed_create_booking_check_out(self) -> None:
        """예약 생성 실패 -> 체크아웃이 오늘 이전일때"""

        url = "/api/bookings/v1/create"
        data = {
            "room_id": self.room.id,
            "guests": 2,
            "check_in": "2023-02-05",
            "check_out": "2023-02-03",
        }
        self.client.force_authenticate(self.guest)
        res = self.client.post(url, data)

        self.assertEqual(res.json()["error_code"], 300004)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2023-01-05", tz_offset=9)
    def test_failed_create_booking_check_date(self) -> None:
        """예약 생성 실패 -> 체크아웃이 체크인보다 이전일때"""

        url = "/api/bookings/v1/create"
        data = {
            "room_id": self.room.id,
            "guests": 2,
            "check_in": "2023-02-05",
            "check_out": "2023-02-03",
        }
        self.client.force_authenticate(self.guest)
        res = self.client.post(url, data)

        self.assertEqual(res.json()["error_code"], 300005)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
