from rest_framework import status
from rest_framework.test import APITestCase


class SignUpTestCase(APITestCase):
    """
    유저 회원가입 테스트케이스
    """

    def setUp(self) -> None:
        self.url = "/api/users/v1/sign-up"

    def test_success_sign_up(self) -> None:
        """회원가입 성공"""
        data = {
            "name": "michael",
            "username": "michael@gmail.com",
            "password": "12345678",
            "password_confirm": "12345678",
            "email": "michael@gmail.com",
            "phone": "01012345678",
        }

        res = self.client.post(self.url, data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_failed_sign_up_pwd(self) -> None:
        """회원가입 실패 -> 비밀번호 미일치"""
        data = {
            "name": "michael",
            "username": "michael@gmail.com",
            "password": "12345678",
            "password_confirm": "123456",
            "email": "michael@gmail.com",
            "phone": "01012345678",
        }

        res = self.client.post(self.url, data, format="json")
        self.assertEqual(res.json().get("error_code"), 100002)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
