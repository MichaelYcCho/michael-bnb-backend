from rest_framework import status
from rest_framework.test import APITestCase

from model_mommy import mommy


class ReviewListTestCase(APITestCase):
    """
    Review 조회 테스트케이스
    """

    def setUp(self) -> None:
        self.owner = mommy.make("users.User")
        self.category = mommy.make("Category", kind="rooms")
        self.room1 = mommy.make(
            "Room", owner=self.owner, name="방1", category=self.category
        )
        self.room2 = mommy.make(
            "Room", owner=self.owner, name="방2", category=self.category
        )
        self.reviewer1 = mommy.make("users.User")
        self.reviewer2 = mommy.make("users.User")
        self.amenity = mommy.make("Amenity", name="TV")
        self.room1.amenities.add(self.amenity)

        self.review1 = mommy.make(
            "Review", room=self.room1, user=self.reviewer1, content="유저1, 방1 리뷰"
        )
        self.review2 = mommy.make(
            "Review", room=self.room1, user=self.reviewer2, content="유저2, 방1 리뷰"
        )
        self.review3 = mommy.make(
            "Review", room=self.room1, user=self.reviewer1, content="리뷰"
        )
        self.review4 = mommy.make(
            "Review", room=self.room1, user=self.reviewer2, content="리뷰"
        )

        self.review5 = mommy.make(
            "Review", room=self.room2, user=self.reviewer1, content="유저2, 방2 리뷰"
        )

    def test_success_get_review_room1(self) -> None:
        """리뷰내역 조회"""

        url = f"/api/reviews/v1/list/{self.room1.id}"
        res = self.client.get(url)

        self.assertEqual(len(res.json()), 3)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        url = f"/api/reviews/v1/list/{self.room2.id}"
        res = self.client.get(url)

        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
