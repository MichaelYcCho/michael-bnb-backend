from django.db import transaction
from rest_framework.exceptions import ParseError
from rest_framework.request import Request

from categories.models import Category
from rooms.models import Amenity, Room


class RoomCreateService:
    def __init__(self, request: Request, data: dict) -> None:
        self.request = request
        self.room_name = data.get("name")
        self.country = data.get("country")
        self.city = data.get("city")
        self.price = data.get("price")
        self.rooms = data.get("rooms")
        self.toilets = data.get("toilets")
        self.description = data.get("description")
        self.pet_friendly = data.get("pet_friendly")
        self.category_id = data.get("category")
        self.amenities_list = data.get("amenities")

    def create_room(self) -> Room:
        category = Category.objects.filter(pk=self.category_id).first()
        if category is None:
            raise ParseError("Category is required.")

        try:
            category = Category.objects.get(pk=self.category_id)
            if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                raise ParseError("The category kind should be 'rooms'")
        except Category.DoesNotExist:
            raise ParseError("Category not found")

        with transaction.atomic():
            owner = self.request.user

            room = Room.objects.create(
                name=self.room_name,
                country=self.country,
                city=self.city,
                price=self.price,
                rooms=self.rooms,
                toilets=self.toilets,
                description=self.description,
                pet_friendly=self.pet_friendly,
                category=category,
                owner=owner,
            )

            for amenity_id in self.amenities_list:
                amenity = Amenity.objects.filter(pk=amenity_id).first()
                if amenity is None:
                    raise ParseError("Amenity not found")
                room.amenities.add(amenity)

        return room
