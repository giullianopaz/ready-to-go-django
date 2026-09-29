from django.contrib import admin
from django.urls import include, path

from apps.core.views import health_check, home

from .api import api

urlpatterns = [
    # Modern Admin (Unfold)
    path("admin/", admin.site.urls),
    # REST API via django-ninja with OpenAPI Swagger at /api/v1/docs
    path("api/v1/", api.urls),
    # Production Health Check probe for Kamal / Docker
    path("up", health_check, name="health-check"),
    # Prometheus Metrics
    path("", include("django_prometheus.urls")),
    # Application Landing Page
    path("", home, name="home"),
]
