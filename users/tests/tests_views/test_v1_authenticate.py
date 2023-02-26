from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAuthTestCase(APITestCase):
    """
    유저 로그인 로그아웃 테스트케이스
    """

    def setUp(self) -> None:
        self.user = User.objects.create(
            name="admin",
            username="admin",
            email="admin@admin.kr",
            phone="01012345678",
        )
        self.user.set_password("admin")
        self.user.save()

    def test_success_sign_up(self) -> None:
        """로그인 성공"""
        url = "/api/users/v1/log-in"
        data = {
            "username": "admin",
            "password": "admin",
        }
        res = self.client.post(url, data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_failed_sign_in_none_field(self) -> None:
        """로그인 실패 -> 필드 미입력"""
        url = "/api/users/v1/log-in"
        data = {
            "username": "",
            "password": "admin",
        }

        res = self.client.post(url, data, format="json")
        self.assertEqual(res.json().get("error_code"), 999999)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
