"""Development settings."""

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# In local non-docker testing, if DB_WORKER is not running, tasks can be executed immediately:
# To use background DB worker, leave TASKS as configured in base.py.
# If immediate execution is desired for local scripts:
# TASKS["default"]["BACKEND"] = "django.tasks.backends.immediate.ImmediateBackend"
