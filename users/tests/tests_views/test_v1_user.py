from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    """
    유저 테스트케이스
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

    def test_success_user_get_self_profile(self) -> None:
        """유저 자기 프로필 조회  ->  성공"""
        url = "/api/users/v1/me"
        user = mommy.make("users.User", name="michael", username="michael@gmail.com")
        self.client.force_authenticate(user)

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_success_user_change_mode(self) -> None:
        """호스트 - 게스트 모드 변경"""
        url = "/api/users/v1/change-mode"
        user = mommy.make("users.User", name="HostMan", username="Host", is_host=True)
        self.client.force_authenticate(user)

        res = self.client.patch(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user.is_host, False)
