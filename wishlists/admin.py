from django.contrib import admin

from wishlists.models.wish_list import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "created",
        "modified",
    )
