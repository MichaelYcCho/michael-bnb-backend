from django.urls import path

from users.views.base_views import ChangePassword, JWTLogIn, PublicUser
from users.views.view_v0_social_login import GithubLogIn, KakaoLogIn
from users.views.view_v1_auth import LogIn, LogOut
from users.views.view_v1_signup import SignUp
from users.views.view_v1_user import ChangeModeAPI, MyProfileAPI

urlpatterns = [
    path("v0/change-password", ChangePassword.as_view()),
    path("v0/jwt-login", JWTLogIn.as_view()),
    path("v0/@<str:username>", PublicUser.as_view()),
    path("v1/sign-up", SignUp.as_view()),
    path("v1/me", MyProfileAPI.as_view()),
    path("v1/change-mode", ChangeModeAPI.as_view()),
    path("v1/log-in", LogIn.as_view()),
    path("v1/log-out", LogOut.as_view()),
    path("v0/github", GithubLogIn.as_view()),
    path("v0/kakao", KakaoLogIn.as_view()),
]
