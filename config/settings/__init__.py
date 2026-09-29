"""Settings module dispatcher."""

import os

env = os.environ.get("DJANGO_ENV", "development").lower()

if env == "production":
    from .production import *
elif env == "test":
    from .test import *
else:
    from .development import *
