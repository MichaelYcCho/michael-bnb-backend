from django.urls import path
from rooms.views.view_v1_amenity import AmenitiesListAPI
from rooms.views.view_v0_room import RoomReviews, RoomAmenities, RoomPhotos
from rooms.views.view_v1_room import (
    RoomsListAPI,
    RoomCreateAPI,
    RoomDetailAPI,
    RoomUpdateAPI,
    RoomDeleteAPI,
)

urlpatterns = [
    path("v1/list", RoomsListAPI.as_view()),
    path("v1/create", RoomCreateAPI.as_view()),
    path("v1/detail/<int:room_id>", RoomDetailAPI.as_view()),
    path("v1/update/<int:room_id>", RoomUpdateAPI.as_view()),
    path("v1/delete/<int:room_id>", RoomDeleteAPI.as_view()),
    path("v0/<int:pk>/reviews", RoomReviews.as_view()),
    path("v0/<int:pk>/amenities", RoomAmenities.as_view()),
    path("v0/<int:pk>/photos", RoomPhotos.as_view()),
    path("v1/amenities/list", AmenitiesListAPI.as_view()),
]
