from django.urls import path

from wishlists.views.view_v1_wish_list import WishlistToggleAPI

urlpatterns = {
    path("toggle/<int:room_id>", WishlistToggleAPI.as_view()),
}
