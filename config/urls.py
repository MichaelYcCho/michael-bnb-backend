from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v0/rooms/", include("rooms.urls")),
    path("api/v0/categories/", include("categories.urls")),
    path("api/v0/experiences/", include("experiences.urls")),
    path("api/v0/medias/", include("medias.urls")),
    path("api/v0/wishlists/", include("wishlists.urls")),
    path("api/v0/users/", include("users.urls")),
    path("api/v0/bookings/", include("bookings.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
