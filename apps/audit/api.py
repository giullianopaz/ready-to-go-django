from datetime import datetime
from uuid import UUID

from ninja import Router, Schema
from ninja.errors import HttpError

from apps.accounts.backends import JWTAuth

from .models import AuditLog

router = Router(tags=["Audit Logs"])


class AuditLogOut(Schema):
    id: UUID
    action: str
    model_name: str
    object_id: str
    changes: dict
    ip_address: str | None
    created_at: datetime


@router.get("/", response=list[AuditLogOut], auth=JWTAuth())
def list_audit_logs(request, limit: int = 50):
    """Retrieve system audit logs (Admin only)."""
    if not request.user.is_superuser:
        raise HttpError(403, "Admin privileges required.")
    return AuditLog.objects.all()[:limit]
