import requests
from django.conf import settings
from django.contrib.auth import login
from rest_framework.request import Request

from users.models import User
from utils.exceptions.exception import UserExceptions


class SocialLoginService:
    def __init__(self, request: Request, data: dict) -> None:
        self.request = request
        self.code = data.get("code")

    def github_login(self) -> bool:
        try:
            code = self.code
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token"
                f"?code={code}&client_id={settings.GH_ID}"
                f"&client_secret={settings.GH_SECRET}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()
            try:
                user = User.objects.get(email=user_emails[0]["email"])  # type: ignore
                login(self.request, user)
                return True

            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),  # type: ignore
                    email=user_emails[0]["email"],  # type: ignore
                    name=user_data.get("name"),  # type: ignore
                    avatar=user_data.get("avatar_url"),  # type: ignore
                    # sns_id = user_data.get("id"), # sns_id 필드로 고유값 저장할것
                )
                user.set_unusable_password()
                # has_usable_password()가 False를 리턴하면 로그인 불가능하는 로직도 가능
                user.save()
                login(self.request, user)
                return True
        except Exception:
            raise UserExceptions.SocialLoginFailed

    def kako_login(self) -> bool:
        try:
            code = self.request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_ID,
                    "redirect_uri": settings.KAKAO_REDIRECT_URI
                    if settings.APP_ENV == "PROD"
                    else "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")  # type: ignore
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(self.request, user)
                return True
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                    # sns_id = user_data.get("id"), # sns_id 필드로 고유값 저장할것
                )
                user.set_unusable_password()
                user.save()
                login(self.request, user)
                return True
        except Exception:
            raise UserExceptions.SocialLoginFailed
