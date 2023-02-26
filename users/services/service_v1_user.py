from django.contrib.auth import authenticate, login
from rest_framework.request import Request

from users.models import User
from utils.exceptions.exception import UserExceptions


class UserService:
    def __init__(self, user: User) -> None:
        self.user = user

    def change_user_mode(self):
        self.user.is_host = not self.user.is_host
        self.user.save()


class UserSignInService:
    def __init__(self, request: Request, data: dict) -> None:
        self.request = request
        self.username = data.get("username")
        self.password = data.get("password")

    def sign_in(self):
        user = authenticate(
            username=self.username,
            password=self.password,
        )

        if user:
            login(self.request, user)
            return user

        raise UserExceptions.UserSignInFailed
