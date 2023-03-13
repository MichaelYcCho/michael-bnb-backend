from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.selectors.selector_v1_category import CategorySelector
from categories.serializers import CategoryListResponseSerializer


class CategoryListAPI(APIView):
    @swagger_auto_schema(
        operation_summary="V1 Category List API",
        operation_description="현재 등록된 카테고리를 조회",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "조회 완료", CategoryListResponseSerializer(many=True)
            ),
        },
    )
    def get(self, request: Request):
        categories = CategorySelector().get_room_category()
        serializer = CategoryListResponseSerializer(categories, many=True)

        return Response(serializer.data)
