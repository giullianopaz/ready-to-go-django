from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TimestampModel, UUIDModel


class User(AbstractUser, UUIDModel, TimestampModel):
    """Custom user model using UUID as primary key and email as unique identity."""

    email = models.EmailField(unique=True, db_index=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.username or self.email
