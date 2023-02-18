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
        self.category = mommy.make("Category", kind="rooms")
        self.amenity = mommy.make("Amenity", name="TV")
        self.room = mommy.make("Room", owner=self.owner, category=self.category)
        self.room.amenities.add(self.amenity)

        self.booking = mommy.make("Booking", room=self.room, user=self.guest)

    def test_success_get_my_booking(self) -> None:
        """내 예약내역 조회"""

        url = "/api/bookings/v1/my"
        self.client.force_authenticate(self.guest)
        res = self.client.get(url)

        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_success_get_my_booking_None(self) -> None:
        """내 예약내역 조회"""
        self.nobody = mommy.make("users.User")
        url = "/api/bookings/v1/my"
        self.client.force_authenticate(self.nobody)
        res = self.client.get(url)

        self.assertEqual(len(res.json()), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_success_get_managing_booking(self) -> None:
        """내 방 예약내역 조회"""

        url = "/api/bookings/v1/manage"
        self.client.force_authenticate(self.owner)
        res = self.client.get(url)

        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
