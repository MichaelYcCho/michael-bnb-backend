from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase


class AmenityListTestCase(APITestCase):
    """
    Amenity List 테스트케이스
    """

    def setUp(self) -> None:
        self.amenity1 = mommy.make("Amenity", name="TV")
        self.amenity2 = mommy.make("Amenity", name="Wifi")
        self.amenity3 = mommy.make("Amenity", name="냉장고")
        self.amenity4 = mommy.make("Amenity", name="에어컨")
        self.amenity5 = mommy.make("Amenity", name="세탁기")
        self.amenity6 = mommy.make("Amenity", name="헤어드라이어")

    def test_success_amenity_list(self) -> None:
        """Amenity List -> 성공"""

        self.url = "/api/rooms/v1/amenities/list"

        res = self.client.get(self.url)
        json = res.json()

        self.assertEqual(len(json), 6)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_success_room_amenity_list(self) -> None:
        """Room 특정 Room에서 가지고 있는 Amenity List -> 성공"""

        self.user = mommy.make("users.User")
        self.category = mommy.make("Category", kind="rooms")
        self.room = mommy.make(
            "Room", owner=self.user, name="방1", category=self.category
        )

        self.room.amenities.add(self.amenity1)
        self.room.amenities.add(self.amenity2)
        self.room.amenities.add(self.amenity3)
        self.room.amenities.add(self.amenity4)
        self.room.amenities.add(self.amenity5)
        self.room.amenities.add(self.amenity6)

        self.url = f"/api/rooms/v1/{self.room.id}/amenities"

        res = self.client.get(self.url)

        json = res.json()

        self.assertEqual(len(json), 4)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
