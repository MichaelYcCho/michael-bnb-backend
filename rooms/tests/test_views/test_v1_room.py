from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from rooms.models.room import Room


class CreateRoomTestCase(APITestCase):
    """
    Room Create 테스트케이스
    """

    def setUp(self) -> None:
        self.user = mommy.make("users.User")
        self.category = mommy.make("Category", kind="rooms")
        self.amenity = mommy.make("Amenity", name="TV")

    def test_success_create_room(self) -> None:
        """Room Create 성공"""

        self.client.force_authenticate(self.user)
        self.url = "/api/rooms/v1/create"

        data = {
            "name": "Michael",
            "country": "Korea",
            "city": "Seoul",
            "address": "srecret",
            "price": "2",
            "rooms": "3",
            "toilets": "1",
            "description": "4",
            "pet_friendly": True,
            "kind": "entire_place",
            "category": f"{self.category.id}",
            "amenities": [f"{self.amenity.id}"],
        }

        res = self.client.post(self.url, data, format="json")
        room = Room.objects.filter(id=res.data["id"]).first()

        self.assertIsNotNone(room)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_fail_category_is_none(self) -> None:
        """카테고리가 없으면 에러 발생"""

        self.client.force_authenticate(self.user)
        self.url = "/api/rooms/v1/create"

        data = {
            "name": "Michael",
            "country": "Korea",
            "city": "Seoul",
            "address": "sercret",
            "price": "2",
            "rooms": "3",
            "toilets": "1",
            "description": "4",
            "pet_friendly": True,
            "kind": "entire_place",
            "amenities": [f"{self.amenity.id}"],
        }

        res = self.client.post(self.url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json().get("error_code"), 999999)

    def test_fail_amenity_is_none(self) -> None:
        """Amenity가 없으면 에러 발생"""

        self.client.force_authenticate(self.user)
        self.url = "/api/rooms/v1/create"

        data = {
            "name": "Michael",
            "country": "Korea",
            "city": "Seoul",
            "address": "sercret",
            "price": "2",
            "rooms": "3",
            "toilets": "1",
            "description": "4",
            "pet_friendly": True,
            "kind": "entire_place",
            "category": "1",
        }

        res = self.client.post(self.url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json().get("error_code"), 999999)


class UpdateRoomTestCase(APITestCase):
    """
    Room Update 테스트케이스
    """

    def setUp(self) -> None:
        self.user = mommy.make("users.User")
        self.category = mommy.make("Category", kind="rooms")
        self.amenity = mommy.make("Amenity", name="TV")
        self.room = mommy.make("Room", owner=self.user, category=self.category)
        self.room.amenities.add(self.amenity)

    def test_success_update_room(self) -> None:
        """Room Update 성공"""

        self.client.force_authenticate(self.user)
        self.url = f"/api/rooms/v1/update/{self.room.id}"
        category_japan = mommy.make("Category", kind="rooms", name="japan")

        data = {
            "room_id": f"{self.room.id}",
            "name": "Michael",
            "country": "Korea",
            "city": "Seoul",
            "address": "secret",
            "price": "1",
            "rooms": "1",
            "toilets": "3",
            "description": "4",
            "pet_friendly": True,
            "kind": "entire_place",
            "category": f"{category_japan.id}",
            "amenities": [f"{self.amenity.id}"],
        }

        res = self.client.put(self.url, data, format="json")
        json = res.json()

        self.assertEqual(json.get("address"), "secret")
        self.assertEqual(json.get("category").get("id"), category_japan.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
