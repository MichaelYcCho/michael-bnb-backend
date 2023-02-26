from django.urls import path

from reviews.views.view_v1_room_reviews import GetRoomReviewAPI

urlpatterns = [
    path("v1/list/<int:room_id>", GetRoomReviewAPI.as_view()),
]
