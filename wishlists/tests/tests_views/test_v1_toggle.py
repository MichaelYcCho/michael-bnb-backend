from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from wishlists.models.wish_list import Wishlist


class WishListToggleTestCase(APITestCase):
    """
    WishList Toggle 테스트케이스
    """

    def setUp(self) -> None:
        self.user = mommy.make("users.User")
        self.category = mommy.make("Category", kind="rooms", name="Country")
        self.amenity = mommy.make("Amenity", name="TV")
        self.room = mommy.make("Room", owner=self.user, category=self.category)
        self.room.amenities.add(self.amenity)

    def test_success_toggle_wish_list(self) -> None:
        """WishList Toggle -> 성공"""

        self.client.force_authenticate(self.user)
        self.url = f"/api/wishlists/v1/toggle/{self.room.id}"

        res = self.client.put(self.url)
        wishlist = Wishlist.objects.filter(user=self.user).first()
        self.assertTrue(wishlist.rooms.filter(id=self.room.id).exists())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.put(self.url)
        wishlist = Wishlist.objects.filter(user=self.user).first()
        self.assertFalse(wishlist.rooms.filter(id=self.room.id).exists())
        self.assertEqual(res.status_code, status.HTTP_200_OK)
