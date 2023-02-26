from django.contrib import admin

from .models.room import Room, Amenity
from .selectors.selector_v1_room import RoomSelector


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "get_total_amenities",
        "get_rating",
        "owner",
        "created",
    )

    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created",
        "modified",
    )
    search_fields = (
        "name",
        "^price",
        "=owner__username",
    )

    def get_total_amenities(self, room: Room):
        return room.amenities.count()

    def get_rating(self, room: Room):
        selector = RoomSelector()
        return selector.get_room_avg_rating(room.pk)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
        "created",
        "modified",
    )
    readonly_fields = (
        "created",
        "modified",
    )
