from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def health_check(request):
    """
    Lightweight healthcheck endpoint for Kamal, Docker, and Kubernetes probes.
    Verifies database connectivity.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
        return JsonResponse({"status": "ok", "database": True}, status=200)
    except Exception as exc:
        return JsonResponse({"status": "error", "database": False, "detail": str(exc)}, status=503)


def home(request):
    """Render application landing page with HTMX and Cotton components."""
    return render(request, "home.html")


def admin_dashboard_callback(request, context):
    """Dashboard metrics callback for django-unfold."""
    from apps.accounts.models import User

    try:
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
    except Exception:
        total_users = 0
        active_users = 0

    context.update(
        {
            "kpi": [
                {
                    "title": "Total Users",
                    "metric": str(total_users),
                    "footer": "Registered accounts",
                },
                {
                    "title": "Active Users",
                    "metric": str(active_users),
                    "footer": "Active status",
                },
                {
                    "title": "Database Engine",
                    "metric": "PostgreSQL 17",
                    "footer": "Connection pooling active",
                },
                {
                    "title": "Task Queue",
                    "metric": "PostgreSQL Queue",
                    "footer": "django.tasks active",
                },
            ],
        }
    )
    return context
