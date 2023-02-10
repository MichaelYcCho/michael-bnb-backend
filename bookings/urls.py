from django.urls import path

from bookings.views import RoomBookings, RoomBookingCheck

urlpatterns = [
    path("<int:room_pk>/check", RoomBookingCheck.as_view()),
    path("<int:room_pk>", RoomBookings.as_view()),
]
