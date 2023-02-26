from django.contrib import admin

from categories.models.category import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "kind",
    )
    list_filter = ("kind",)
