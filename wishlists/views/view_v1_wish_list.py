from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from wishlists.models.wish_list import Wishlist


class WishlistToggleAPI(APIView):
    @swagger_auto_schema(
        operation_summary="V1 Room List API",
        operation_description="현재 등록된 모든 방을 조회",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "변경 완료",
            ),
        },
    )
    def put(self, request: Request, room_id: int):
        wishlist = Wishlist.objects.filter(user=request.user).first()

        if wishlist is None:
            wishlist = Wishlist.objects.create(
                user=request.user, name=f"{request.user.name} 님의 찜 목록"
            )

        room = self.get_room(room_id)
        if wishlist.rooms.filter(pk=room_id).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)
