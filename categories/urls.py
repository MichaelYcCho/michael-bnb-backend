from django.urls import path

from categories.views import CategoryListAPI

urlpatterns = [
    path("v1/list", CategoryListAPI.as_view()),
]
