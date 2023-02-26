from django.db.models import QuerySet

from categories.models.category import Category
from utils.choices.choice import CategoryKindChoices


class CategorySelector:
    def __init__(self):
        pass

    @staticmethod
    def get_room_category() -> QuerySet[Category]:
        queryset = Category.objects.filter(
            kind=CategoryKindChoices.ROOMS,
        )
        return queryset
