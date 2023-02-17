from rest_framework import status
from rest_framework.test import APITestCase

from model_mommy import mommy

from rooms.models import Room


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

        self.client.force_authenticate(self.guest)
        self.url = "/api/bookings/v1/my"

        res = self.client.get(self.url)

        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_success_get_my_booking_None(self) -> None:
        """내 예약내역 조회"""
        self.nobody = mommy.make("users.User")

        self.client.force_authenticate(self.nobody)
        self.url = "/api/bookings/v1/my"

        res = self.client.get(self.url)

        self.assertEqual(len(res.json()), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
