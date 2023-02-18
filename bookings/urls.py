from django.urls import path

from bookings.views.view_v1_booking import (
    CheckBookingAPI,
    CreateBookingsAPI,
    GetMyBookingsAPI,
    CancelBookingAPI,
    ManageBookingsAPI,
)

urlpatterns = [
    path("v1/create", CreateBookingsAPI.as_view()),
    path("v1/my", GetMyBookingsAPI.as_view()),
    path("v1/manage", ManageBookingsAPI.as_view()),
    path("v1/cancel/<int:booking_id>", CancelBookingAPI.as_view()),
    path("v1/check/<int:room_id>", CheckBookingAPI.as_view()),
]
