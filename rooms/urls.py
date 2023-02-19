from django.urls import path
from rooms.views.view_v0_amenity import Amenities, AmenityDetail
from rooms.views.view_v1_room import (
    RoomsListAPI,
    RoomCreateAPI,
    RoomDetail,
    RoomReviews,
    RoomAmenities,
    RoomPhotos,
)

urlpatterns = [
    path("v1/list", RoomsListAPI.as_view()),
    path("v1/create", RoomCreateAPI.as_view()),
    path("v0/<int:pk>", RoomDetail.as_view()),
    path("v0/<int:pk>/reviews", RoomReviews.as_view()),
    path("v0/<int:pk>/amenities", RoomAmenities.as_view()),
    path("v0/<int:pk>/photos", RoomPhotos.as_view()),
    path("v0/amenities/all", Amenities.as_view()),
    path("v0/amenities/<int:pk>", AmenityDetail.as_view()),
]
