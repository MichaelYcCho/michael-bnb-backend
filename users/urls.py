from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from users.views.base_views import (
    ChangeModeAPI,
    ChangePassword,
    JWTLogIn,
    LogIn,
    LogOut,
    PublicUser,
)
from users.views.view_v0_signup import SignUp
from users.views.view_v0_social_login import GithubLogIn, KakaoLogIn
from users.views.view_v1_user import MyProfileAPI

urlpatterns = [
    path("v0/sign-up", SignUp.as_view()),
    path("v1/me", MyProfileAPI.as_view()),
    path("v0/change-mode", ChangeModeAPI.as_view()),
    path("v0/change-password", ChangePassword.as_view()),
    path("v0/log-in", LogIn.as_view()),
    path("v0/log-out", LogOut.as_view()),
    path("v0/token-login", obtain_auth_token),
    path("v0/jwt-login", JWTLogIn.as_view()),
    path("v0/github", GithubLogIn.as_view()),
    path("v0/kakao", KakaoLogIn.as_view()),
    path("v0/@<str:username>", PublicUser.as_view()),
]
