from rest_framework import status
from rest_framework.test import APITestCase

from model_mommy import mommy


class AmenityListTestCase(APITestCase):
    """
    Amenity List 테스트케이스
    """

    def setUp(self) -> None:
        mommy.make("Amenity", name="TV")
        mommy.make("Amenity", name="Wifi")

    def test_success_amenity_list(self) -> None:
        """Amenity Room List 성공"""

        self.url = "/api/rooms/v1/amenities/list"

        res = self.client.get(self.url)
        json = res.json()

        self.assertEqual(len(json), 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
