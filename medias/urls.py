from django.urls import path

from medias.views import GetUploadURL, PhotoDetail

urlpatterns = [
    path("photos/get-url", GetUploadURL.as_view()),
    path("photos/<int:pk>", PhotoDetail.as_view()),
]
