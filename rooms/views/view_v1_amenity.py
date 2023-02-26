from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from rooms.models import Amenity
from rooms.selectors.selector_v1_room import RoomSelector
from rooms.serializers import AmenityListSerializer
from utils.paginations import RoomAmenitiesPagination


class AmenitiesListAPI(APIView):
    @swagger_auto_schema(
        operation_summary="V1 Amenity List API",
        operation_description="현재 등록된 Amenity 조회",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "조회 완료", AmenityListSerializer(many=True)
            ),
        },
    )
    def get(self, request: Request):
        all_amenities = Amenity.objects.all()
        serializer = AmenityListSerializer(all_amenities, many=True)
        return Response(serializer.data)


class RoomAmenitiesAPI(APIView):
    pagination_class = RoomAmenitiesPagination

    @swagger_auto_schema(
        operation_summary="V1 Room Amenities API",
        operation_description="현재 Room에 등록된 Amenity 조회",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "조회 완료", AmenityListSerializer(many=True)
            ),
        },
    )
    def get(self, request: Request, room_id: int):
        selector = RoomSelector(request)
        room = selector.get_room(room_id)
        amenities = room.amenities.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(amenities, request, view=self)
        output_serializer = AmenityListSerializer(page, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
