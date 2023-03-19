from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.schema import CategoryListOutput
from categories.selectors.selector_v1_category import CategorySelector
from categories.serializers import CategoryListOutputSerializer


class CategoryListAPI(APIView):
    @swagger_auto_schema(
        operation_summary="V2 Category List API",
        operation_description="현재 등록된 카테고리를 조회(Pydantic 모델 사용)",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "조회 완료", CategoryListOutputSerializer(many=True)
            ),
        },
    )
    def get(self, request):
        categories = CategorySelector().get_room_category()
        category_list = list(categories.values())

        # Pydantic 모델로 변환
        category_list_output = [
            CategoryListOutput(**category) for category in category_list
        ]

        # Pydantic 모델을 dict로 변환
        category_list_dict = [category.dict() for category in category_list_output]

        return Response(category_list_dict)
