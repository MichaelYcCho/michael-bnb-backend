from django.urls import path
from . import views
from .views import RoomsListAPI, RoomCreateAPI

urlpatterns = [
    path("list", RoomsListAPI.as_view()),
    path("create", RoomCreateAPI.as_view()),
    path("<int:pk>", views.RoomDetail.as_view()),
    path("<int:pk>/reviews", views.RoomReviews.as_view()),
    path("<int:pk>/amenities", views.RoomAmenities.as_view()),
    path("<int:pk>/photos", views.RoomPhotos.as_view()),
    path("amenities/all", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
]
