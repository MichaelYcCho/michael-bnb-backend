from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from wishlists.services.service_v1_wish_list import WishlistService


class WishlistToggleAPI(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="V1 WishList Toggle API",
        operation_description="찜 목록에 방을 추가 또는 제거",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "변경 완료",
            ),
        },
    )
    def put(self, request: Request, room_id: int):
        service = WishlistService(request)
        service.toggle_wish_list(room_id)
        return Response(status=HTTP_200_OK)
