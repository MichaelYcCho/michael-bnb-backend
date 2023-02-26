from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import SignUpInputSerializer
from users.services.service_v1_sign_up import SignUpService


class SignUp(APIView):
    @swagger_auto_schema(
        operation_summary="V1 Sign-Up API",
        operation_description="회원가입",
        responses={
            status.HTTP_201_CREATED: openapi.Response("가입 완료"),
        },
    )
    def post(self, request: Request):
        serializer = SignUpInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = SignUpService(serializer.validated_data)
        service.validate_password()
        service.create_user()

        return Response(status=status.HTTP_201_CREATED)
