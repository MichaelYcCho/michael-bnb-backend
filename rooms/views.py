from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from .models import Amenity, Room
from categories.models import Category
from . import serializers
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from .selectors.selector_v0_room import RoomSelector
from .serializers import RoomListOutputSerializer
from .services.service_v1_room import RoomCreateService


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = serializers.AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                serializers.AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = serializers.AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = serializers.AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                serializers.AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


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


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="V1 Room Detail API",
        operation_description="특정 방을 조회",
        responses={
            status.HTTP_200_OK: openapi.Response("조회 완료"),
        },
    )
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = serializers.RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="V1 Room Update API",
        operation_description="id를 전달받아 해당 Room을 수정",
        responses={
            status.HTTP_200_OK: openapi.Response("수정 완료"),
        },
    )
    def put(self, request, pk):
        selector = RoomSelector()
        room = selector.get_room(pk)

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


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomAmenities(APIView):
    def get(self, request, pk):
        selector = RoomSelector()
        room = selector.get_room(pk)
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        serializer = serializers.AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
