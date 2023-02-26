from django.db import models
from model_utils.models import TimeStampedModel

from utils.choices import CategoryKindChoices


class Category(TimeStampedModel):
    """Room or Experience Category"""

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}"

    class Meta:
        verbose_name_plural = "Categories"
