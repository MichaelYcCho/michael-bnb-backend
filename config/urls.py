from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

permission = (
    settings.APP_ENV in ("DEV",) and permissions.AllowAny or permissions.IsAuthenticated
)

schema_view = get_schema_view(
    openapi.Info(
        title="Michael-bnb API",
        default_version="v0.1",
        description="Michael-bnb BE API",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    validators=["flex", "ssv"],
    public=True,
    permission_classes=[permission],
)

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


urlpatterns += [
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^documents/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
