from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from utils.choices.choice import CategoryKindChoices


class CategoryListTestCase(APITestCase):
    """
    Category List 테스트케이스
    """

    def setUp(self) -> None:
        mommy.make("Category", kind=CategoryKindChoices.ROOMS)
        mommy.make("Category", kind=CategoryKindChoices.ROOMS)
        mommy.make("Category", kind=CategoryKindChoices.ROOMS)
        mommy.make("Category", kind=CategoryKindChoices.ROOMS)
        mommy.make("Category", kind=CategoryKindChoices.ROOMS)
        mommy.make("Category", kind=CategoryKindChoices.EXPERIENCES)

    def test_success_category_list(self) -> None:
        """Category Room List 성공"""

        self.url = "/api/categories/v1/list"

        res = self.client.get(self.url)
        json = res.json()

        self.assertEqual(len(json), 5)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
