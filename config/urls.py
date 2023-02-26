from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

permission = (
    settings.APP_ENV in ("DEV",)
    and permissions.AllowAny  # or permissions.IsAuthenticated
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
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/rooms/", include("rooms.urls")),
    path("api/reviews/", include("reviews.urls")),
    path("api/categories/", include("categories.urls")),
    path("api/experiences/v0/", include("experiences.urls")),
    path("api/medias/v0/", include("medias.urls")),
    path("api/wishlists/v0/", include("wishlists.urls")),
    path("api/users/", include("users.urls")),
    path("api/bookings/", include("bookings.urls")),
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
