"""Base Django settings for ready-to-go-django."""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1", "web"]),
    POSTGRES_DB=(str, "django_db"),
    POSTGRES_USER=(str, "django"),
    POSTGRES_HOST=(str, "db"),
    POSTGRES_PORT=(int, 5432),
    SMTP_HOST=(str, "mailpit"),
    SMTP_PORT=(int, 1025),
    EMAILS_FROM=(str, "noreply@example.com"),
    JWT_ACCESS_MINUTES=(int, 30),
    JWT_REFRESH_DAYS=(int, 7),
    OTEL_ENABLED=(bool, False),
)

# Read .env if present
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY", default="django-insecure-dev-key-change-in-production")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition
INSTALLED_APPS = [
    # Modern Admin (MUST precede django.contrib.admin)
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Interactivity & Components
    "django_htmx",
    "django_cotton",
    "neapolitan",
    # Task Queue (PostgreSQL-backed)
    "django_tasks",
    "django_tasks_db",
    # Observability & Metrics
    "django_structlog",
    "django_prometheus",
    "django_extensions",
    # Project Apps
    "apps.core",
    "apps.accounts",
    "apps.audit",
    "apps.observability",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
    "apps.core.middleware.RequestIDMiddleware",
    "apps.core.middleware.ProcessTimeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "apps.core.middleware.HtmxVaryMiddleware",
    "apps.audit.middleware.AuditContextMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database (PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="postgres"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
        "CONN_MAX_AGE": 600,
        "CONN_HEALTH_CHECKS": True,
    }
}

# Cache (PostgreSQL Database Cache — UNLOGGED table behavior)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
        "TIMEOUT": 300,
        "OPTIONS": {
            "MAX_ENTRIES": 10000,
            "CULL_FREQUENCY": 3,
        },
    }
}

# Background Tasks (PostgreSQL Database Queue via django-tasks)
TASKS = {
    "default": {
        "BACKEND": "django_tasks_db.DatabaseBackend",
        "QUEUES": ["default", "emails", "reports", "ai_processing"],
    }
}

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Password validation & Modern Argon2 hashing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email Configuration (Mailpit by default in development)
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "HOST": env("SMTP_HOST"),
        "PORT": env("SMTP_PORT"),
        "USE_TLS": False,
    }
}
DEFAULT_FROM_EMAIL = env("EMAILS_FROM")

# JWT Settings for django-ninja API
JWT_SECRET_KEY = env("JWT_SECRET_KEY", default=SECRET_KEY)
JWT_ACCESS_MINUTES = env("JWT_ACCESS_MINUTES")
JWT_REFRESH_DAYS = env("JWT_REFRESH_DAYS")

# Modern Admin Theme: django-unfold
UNFOLD = {
    "SITE_TITLE": "Ready to Go Django",
    "SITE_HEADER": "Admin Dashboard",
    "SITE_SUBHEADER": "The Majestic Monolith",
    "SITE_SYMBOL": "rocket_launch",
    "COLORS": {
        "primary": {
            "50": "#eff6ff",
            "100": "#dbeafe",
            "200": "#bfdbfe",
            "300": "#93c5fd",
            "400": "#60a5fa",
            "500": "#3b82f6",
            "600": "#2563eb",
            "700": "#1d4ed8",
            "800": "#1e40af",
            "900": "#1e3a5f",
            "950": "#172554",
        },
    },
    "DASHBOARD_CALLBACK": "apps.core.views.admin_dashboard_callback",
}

# OpenTelemetry configuration
OTEL_ENABLED = env("OTEL_ENABLED")
OTEL_SERVICE_NAME = env("OTEL_SERVICE_NAME", default="ready-to-go-django")
