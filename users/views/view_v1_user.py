from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserOutputSerializer
from users.services.service_v1_user import UserService


class MyProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="V1 My Information API",
        operation_description="로그인 유저의 정보 조회",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "조회 완료", UserOutputSerializer(many=True)
            ),
        },
    )
    def get(self, request: Request):
        user = request.user
        output_serializer = UserOutputSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class ChangeModeAPI(APIView):
    @swagger_auto_schema(
        operation_summary="V1 Change User Mode API",
        operation_description="호스트-게스트 모드 변경",
        responses={
            status.HTTP_200_OK: openapi.Response("변경 완료"),
        },
    )
    def patch(self, request: Request):
        service = UserService(request.user)
        service.change_user_mode()

        return Response(status=status.HTTP_200_OK)
