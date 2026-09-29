from django.db import models

from apps.core.models import TimestampModel, UUIDModel


class AuditLog(UUIDModel, TimestampModel):
    """Immutable audit trail for model mutations and system actions."""

    ACTION_CHOICES = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("AUTH_LOGIN", "Login"),
        ("AUTH_LOGOUT", "Logout"),
    ]

    action = models.CharField(max_length=50, choices=ACTION_CHOICES, db_index=True)
    model_name = models.CharField(max_length=100, blank=True, db_index=True)
    object_id = models.CharField(max_length=255, blank=True)
    changes = models.JSONField(default=dict, blank=True)
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self) -> str:
        return f"[{self.action}] {self.model_name}:{self.object_id} at {self.created_at}"
