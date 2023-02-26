from django.contrib.auth import logout
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSignInInputSerializer
from users.services.service_v1_user import UserSignInService
from utils.exceptions.exception import UserExceptions


class LogIn(APIView):
    @swagger_auto_schema(
        operation_summary="V1 Sign In API",
        operation_description="로그인 API",
        responses={
            status.HTTP_200_OK: openapi.Response("로그인 완료"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                " or ".join(
                    [
                        UserExceptions.UserInfoDoesNotExist.default_detail,
                        UserExceptions.UserSignInFailed.default_detail,
                    ]
                )
            ),
        },
    )
    def post(self, request: Request):
        input_serializer = UserSignInInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        service = UserSignInService(request, input_serializer.validated_data)
        service.sign_in()
        return Response(status=status.HTTP_200_OK)


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="V1 Sign Out API",
        operation_description="로그아웃 API",
        responses={
            status.HTTP_200_OK: openapi.Response("로그아웃 완료"),
        },
    )
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
