import structlog
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

logger = structlog.get_logger(__name__)


def setup_tracing(service_name: str = "ready-to-go-django", enabled: bool = False):
    """Initialize OpenTelemetry tracer provider and automatic instrumentations."""
    if not enabled:
        return

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    try:
        from opentelemetry.instrumentation.django import DjangoInstrumentor

        DjangoInstrumentor().instrument()
    except Exception as exc:
        logger.warning("Could not instrument Django with OpenTelemetry", error=str(exc))

    try:
        from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor

        PsycopgInstrumentor().instrument()
    except Exception as exc:
        logger.warning("Could not instrument Psycopg with OpenTelemetry", error=str(exc))
