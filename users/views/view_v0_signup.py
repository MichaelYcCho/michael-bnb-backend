from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.serializers import SignUpInputSerializer
from users.services.service_v0_sign_up import SignUpService


class SignUp(APIView):
    def post(self, request):

        serializer = SignUpInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = SignUpService(serializer.validated_data)
        service.validate_password()
        service.create_user()

        return Response(status=status.HTTP_201_CREATED)
