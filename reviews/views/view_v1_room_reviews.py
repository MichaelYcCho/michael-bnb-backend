from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.serializers import ReviewListOutputSerializer
from rooms.selectors.selector_v1_room import RoomSelector
from utils.paginations import RoomReviewPagination


class GetRoomReviewAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = RoomReviewPagination

    @swagger_auto_schema(
        operation_summary="V1 Review List API",
        operation_description="현재 조회한 room의 review를 조회",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "조회 완료", ReviewListOutputSerializer(many=True)
            ),
        },
    )
    def get(self, request: Request, room_id: int) -> Response:
        room = RoomSelector(request).get_room(room_id)
        review = room.reviews.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(review, request, view=self)
        serializer = ReviewListOutputSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
