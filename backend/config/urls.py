from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    path("api/", include("events.api.urls")),
    path("api/", include("orders.api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("payments.api.urls")),
    path("", include("payments.api.urls")),
    path("api/", include("payments.api.urls")),
    path("api/", include("checkin.api.urls")),
    path("api/", include("auth_api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
