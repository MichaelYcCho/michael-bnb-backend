from rest_framework import status
from rest_framework.test import APITestCase

from model_mommy import mommy


class BookingTestCase(APITestCase):
    """
    Booking 테스트케이스
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

    def test_fail_cancel_wrong_booking(self) -> None:
        """예약 취소 실패 -> 존재하지않는 예약번호"""

        url = f"/api/bookings/v1/cancel/99999"
        self.client.force_authenticate(self.guest)
        res = self.client.patch(url)

        self.assertEqual(res.json()["error_code"], 300000)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_fail_cancel_not_matching_booking_user(self) -> None:
        """예약 취소 실패 -> 예약자와 취소 요청자가 다름"""

        url = f"/api/bookings/v1/cancel/{self.booking.id}"
        self.client.force_authenticate(self.nobody)
        res = self.client.patch(url)

        self.assertEqual(res.json()["error_code"], 300001)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_cancel_booking(self) -> None:
        """예약 취소 실패 -> 이미 취소된 예약"""
        self.booking.is_canceled = True
        self.booking.save()

        url = f"/api/bookings/v1/cancel/{self.booking.id}"
        self.client.force_authenticate(self.nobody)
        res = self.client.patch(url)

        self.assertEqual(res.json()["error_code"], 300000)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
