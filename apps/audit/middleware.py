import contextvars

current_user_var = contextvars.ContextVar("current_user", default=None)
current_ip_var = contextvars.ContextVar("current_ip", default=None)
current_ua_var = contextvars.ContextVar("current_ua", default=None)


class AuditContextMiddleware:
    """Capture request context into contextvars for audit attribution."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            current_user_var.set(user)
        else:
            current_user_var.set(None)

        # Extract client IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        current_ip_var.set(ip)

        current_ua_var.set(request.META.get("HTTP_USER_AGENT", ""))

        response = self.get_response(request)

        # Clear contextvars
        current_user_var.set(None)
        current_ip_var.set(None)
        current_ua_var.set(None)

        return response
