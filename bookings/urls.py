from django.urls import path

from bookings.views.view_v0_booking import RoomBookingCheck, RoomBookings, GetMyBookings

urlpatterns = [
    path("my", GetMyBookings.as_view()),
    path("<int:room_pk>/check", RoomBookingCheck.as_view()),
    path("<int:room_pk>", RoomBookings.as_view()),
]
