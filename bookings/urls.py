from django.urls import path

from bookings.views.view_v0_booking import (
    CheckBookingAPI,
    CreateBookingsAPI,
    GetMyBookingsAPI,
    CancelBookingAPI,
)

urlpatterns = [
    path("my", GetMyBookingsAPI.as_view()),
    path("cancel/<int:booking_id>", CancelBookingAPI.as_view()),
    path("<int:room_pk>/check", CheckBookingAPI.as_view()),
    path("<int:room_pk>", CreateBookingsAPI.as_view()),
]
