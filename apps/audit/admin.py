from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = ["action", "model_name", "object_id", "user", "ip_address", "created_at"]
    list_filter_submit = True
    list_filter = ["action", "model_name", ("created_at", RangeDateFilter)]
    search_fields = ["model_name", "object_id", "user__email", "ip_address"]
    readonly_fields = [
        "id",
        "action",
        "model_name",
        "object_id",
        "changes",
        "user",
        "ip_address",
        "user_agent",
        "created_at",
        "updated_at",
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
