from django.urls import path

from rooms.views.view_v1_amenity import AmenitiesListAPI, RoomAmenitiesAPI
from rooms.views.view_v1_room import (
    RoomCreateAPI,
    RoomCreatePhotosAPI,
    RoomDeleteAPI,
    RoomDetailAPI,
    RoomsListAPI,
    RoomUpdateAPI,
)

urlpatterns = [
    path("v1/list", RoomsListAPI.as_view()),
    path("v1/create", RoomCreateAPI.as_view()),
    path("v1/detail/<int:room_id>", RoomDetailAPI.as_view()),
    path("v1/update/<int:room_id>", RoomUpdateAPI.as_view()),
    path("v1/delete/<int:room_id>", RoomDeleteAPI.as_view()),
    path("v1/<int:room_id>/amenities", RoomAmenitiesAPI.as_view()),
    path("v1/<int:room_id>/photos", RoomCreatePhotosAPI.as_view()),
    path("v1/amenities/list", AmenitiesListAPI.as_view()),
]
