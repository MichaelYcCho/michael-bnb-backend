from django.urls import path

from categories.views.view_v1_category import CategoryListAPI as CategoryListAPIV1
from categories.views.view_v2_category import CategoryListAPI as CategoryListAPIV2

urlpatterns = [
    path("v1/list", CategoryListAPIV1.as_view()),
    path("v2/list", CategoryListAPIV2.as_view()),
]
