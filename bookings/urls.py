from django.urls import path

from bookings.views.view_v0_booking import (
    CheckBookingAPI,
    CreateBookingsAPI,
    GetMyBookingsAPI,
    CancelBookingAPI,
    ManageBookingsAPI,
)

urlpatterns = [
    path("my", GetMyBookingsAPI.as_view()),
    path("manage", ManageBookingsAPI.as_view()),
    path("cancel/<int:booking_id>", CancelBookingAPI.as_view()),
    path("<int:room_id>/check", CheckBookingAPI.as_view()),
    path("<int:room_id>", CreateBookingsAPI.as_view()),
]
