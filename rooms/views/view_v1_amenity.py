from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rooms.models import Amenity
from rooms.serializers import AmenityListInputSerializer


class AmenitiesListAPI(APIView):
    @swagger_auto_schema(
        operation_summary="V1 Amenity List API",
        operation_description="현재 등록된 Amenity 조회",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "조회 완료", AmenityListInputSerializer(many=True)
            ),
        },
    )
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenityListInputSerializer(all_amenities, many=True)
        return Response(serializer.data)
