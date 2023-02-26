from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from medias.serializers import PhotoCreateSerializer
from medias.services.service_v1_photo import PhotoService
from rooms import serializers
from rooms.selectors.selector_v1_room import RoomSelector
from rooms.serializers import (
    RoomDetailOutputSerializer,
    RoomListOutputSerializer,
    RoomUpdateInputSerializer,
)
from rooms.services.service_v1_room import RoomDeleteService, RoomService
from utils.exceptions.exception import RoomExceptions


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
        service = RoomService(request, input_serializer.validated_data)
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
        input_serializer = RoomUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        selector = RoomSelector()
        room = selector.get_room(room_id)
        service = RoomService(request, input_serializer.validated_data)
        service.update_room(room)

        output_serializer = RoomDetailOutputSerializer(room)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class RoomDeleteAPI(APIView):
    # TODO: Owner Permission
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="V1 Room Delete API",
        operation_description="id를 전달받아 해당 Room을 삭제",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("삭제 완료"),
        },
    )
    def delete(self, request: Request, room_id: int):
        selector = RoomSelector(request)
        room = selector.get_room(room_id)

        service = RoomDeleteService(request, room)
        service.delete_room()

        return Response(status=HTTP_204_NO_CONTENT)


class RoomCreatePhotosAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="V1 Room Photo Create API",
        operation_description="Photo 정보를 받아 저장후 해당 Room에 매핑",
        responses={
            status.HTTP_200_OK: openapi.Response("매핑 완료"),
        },
    )
    def post(self, request: Request, room_id: int) -> Response:
        room = RoomSelector(request).get_room(room_id)

        if request.user != room.owner:
            raise RoomExceptions.UserIsNotOwner

        input_serializer = PhotoCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        service = PhotoService(request, input_serializer.validated_data)
        photo = service.create_photo(room)
        output_serializer = PhotoCreateSerializer(photo)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
