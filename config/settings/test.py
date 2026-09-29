"""Testing settings for pytest."""

import os

from .base import *

DEBUG = False
SECRET_KEY = "test-secret-key-for-pytest-runs-only"

# Fast password hasher for tests (100x faster than Argon2)
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Database configuration for tests:
# Defaults to in-memory SQLite for instant isolated unit/integration tests
if os.environ.get("USE_POSTGRES_TEST") == "1":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "test_django_db",
            "USER": "django",
            "PASSWORD": "test_password",
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }

# Tasks Dummy Backend for tests
TASKS = {
    "default": {
        "BACKEND": "django.tasks.backends.dummy.DummyBackend",
        "QUEUES": ["default", "emails", "reports", "ai_processing"],
    }
}

# In-memory cache for tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "test-cache",
    }
}

# Modern Django 6 MAILERS for tests
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    }
}
