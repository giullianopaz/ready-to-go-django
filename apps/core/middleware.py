import time
import uuid


class RequestIDMiddleware:
    """Extract or generate X-Request-ID for distributed tracing."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.request_id = request_id

        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        return response


class ProcessTimeMiddleware:
    """Measure request processing duration and set X-Process-Time-Ms header."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start_time) * 1000
        response["X-Process-Time-Ms"] = f"{duration_ms:.2f}"
        return response


class HtmxVaryMiddleware:
    """Ensure CDNs and reverse proxies cache full-page and HTMX partial responses separately."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        existing_vary = response.get("Vary", "")
        if "HX-Request" not in existing_vary:
            response["Vary"] = f"{existing_vary}, HX-Request".strip(", ")
        return response
