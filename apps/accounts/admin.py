from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter

from .models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ["username", "email", "is_staff", "is_superuser", "is_active", "created_at"]
    search_fields = ["username", "email", "first_name", "last_name"]
    list_filter_submit = True
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
        ("created_at", RangeDateFilter),
    ]
    readonly_fields = ["id", "created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Metadata", {"fields": ("id", "last_login", "last_login_ip", "created_at", "updated_at")}),
    )


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
