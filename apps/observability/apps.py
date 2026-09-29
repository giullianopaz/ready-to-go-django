from django.apps import AppConfig
from django.conf import settings


class ObservabilityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.observability"
    verbose_name = "Observability"

    def ready(self):
        from .logging import setup_logging
        from .tracing import setup_tracing

        setup_logging(debug=settings.DEBUG)
        setup_tracing(
            service_name=getattr(settings, "OTEL_SERVICE_NAME", "ready-to-go-django"),
            enabled=getattr(settings, "OTEL_ENABLED", False),
        )
