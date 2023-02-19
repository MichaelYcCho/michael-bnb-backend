from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from rooms.models import Amenity, Room
from categories.models import Category
from rooms import serializers
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from rooms.selectors.selector_v0_room import RoomSelector
from rooms.serializers import RoomListOutputSerializer, RoomDetailOutputSerializer
from rooms.services.service_v1_room import RoomCreateService


class RoomsListAPI(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="V1 Room List API",
        operation_description="현재 등록된 모든 방을 조회",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "조회 완료", RoomListOutputSerializer(many=True)
            ),
        },
    )
    def get(self, request: Request):

        rooms = RoomSelector(request).get_all_rooms()
        serializer = RoomListOutputSerializer(rooms, many=True)

        return Response(serializer.data)


class RoomCreateAPI(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="V1 Room Create API",
        operation_description="새로운 방을 생성",
        request_body=serializers.RoomCreateInputSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response("생성 완료"),
        },
    )
    def post(self, request):
        input_serializer = serializers.RoomCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        service = RoomCreateService(request, input_serializer.validated_data)
        room = service.create_room()
        output_serializer = serializers.RoomCreateOutputSerializer({"id": room.id})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class RoomDetailAPI(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="V1 Room Detail API",
        operation_description="특정 방을 조회",
        responses={
            status.HTTP_200_OK: openapi.Response("조회 완료"),
        },
    )
    def get(self, request: Request, room_id: int):
        selector = RoomSelector(request)
        room = selector.get_room(room_id)
        serializer = RoomDetailOutputSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomUpdateAPI(APIView):

    # TODO: Owner Permission

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="V1 Room Update API",
        operation_description="id를 전달받아 해당 Room을 수정",
        responses={
            status.HTTP_200_OK: openapi.Response("수정 완료"),
        },
    )
    def put(self, request: Request, room_id: int):
        selector = RoomSelector()
        room = selector.get_room(room_id)

        if not room.owner == request.user:
            raise PermissionDenied
        serializer = serializers.RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The Category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
            amenities = request.data.get("amenities")
            if amenities:
                for amenity_pk in amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                    except Amenity.DoesNotExist:
                        raise ParseError(f"Amenity with id {amenity_pk} not found")
                room.amenities.set(amenities)
            updated_room = serializer.save()
            serializer = serializers.RoomDetailSerializer(
                updated_room,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="V1 Room Delete API",
        operation_description="id를 전달받아 해당 Room을 삭제",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("삭제 완료"),
        },
    )
    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
