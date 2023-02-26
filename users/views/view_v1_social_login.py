from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSocialLoginInputSerializer
from users.services.service_v1_social_login import SocialLoginService


class GithubLogIn(APIView):
    @swagger_auto_schema(
        operation_summary="V1 GitHub Login API",
        operation_description="깃허브 로그인 API",
        responses={
            status.HTTP_200_OK: openapi.Response("로그인 성공"),
        },
    )
    def post(self, request: Request) -> Response:
        input_serializer = UserSocialLoginInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        service = SocialLoginService(request, input_serializer.validated_data)
        service.github_login()
        return Response(status=status.HTTP_200_OK)


class KakaoLogIn(APIView):
    @swagger_auto_schema(
        operation_summary="V1 KaKao Login API",
        operation_description="카카오 로그인 API",
        responses={
            status.HTTP_200_OK: openapi.Response("로그인 성공"),
        },
    )
    def post(self, request: Request) -> Response:
        input_serializer = UserSocialLoginInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        service = SocialLoginService(request, input_serializer.validated_data)
        service.kako_login()
        return Response(status=status.HTTP_200_OK)
