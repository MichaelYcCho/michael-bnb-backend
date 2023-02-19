from django.urls import path
from . import views
from rooms.views import RoomsListAPI, RoomCreateAPI


urlpatterns = [
    path("v0/list", RoomsListAPI.as_view()),
    path("v1/create", RoomCreateAPI.as_view()),
    path("v0/<int:pk>", views.RoomDetail.as_view()),
    path("v0/<int:pk>/reviews", views.RoomReviews.as_view()),
    path("v0/<int:pk>/amenities", views.RoomAmenities.as_view()),
    path("v0/<int:pk>/photos", views.RoomPhotos.as_view()),
    path("v0/amenities/all", views.Amenities.as_view()),
    path("v0/amenities/<int:pk>", views.AmenityDetail.as_view()),
]
