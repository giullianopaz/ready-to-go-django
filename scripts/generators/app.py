#!/usr/bin/env python3
"""
Rails/Phoenix-like Django App Generator.

Usage:
    python -m scripts.generators.app <app_name>
    make generate-app name=<app_name>
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = ROOT_DIR / "apps"

BLUE = "\033[36m"
GREEN = "\033[32m"
BOLD = "\033[1m"
RESET = "\033[0m"


def generate_app(app_name: str) -> None:
    app_name = app_name.lower().strip()
    target_dir = APPS_DIR / app_name
    class_name = "".join(word.capitalize() for word in app_name.split("_"))

    if target_dir.exists():
        print(f"Error: App '{app_name}' already exists at {target_dir}")
        sys.exit(1)

    print(f"\n{BOLD}{BLUE}Scaffolding new Django App:{RESET} {BOLD}{app_name}{RESET}")

    target_dir.mkdir(parents=True)
    tests_dir = target_dir / "tests"
    tests_dir.mkdir(parents=True)

    # 1. __init__.py
    (target_dir / "__init__.py").write_text("")

    # 2. apps.py
    (target_dir / "apps.py").write_text(
        f"""from django.apps import AppConfig


class {class_name}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.{app_name}"
"""
    )

    # 3. models.py
    (target_dir / "models.py").write_text(
        """from django.db import models
from apps.core.models import UUIDModel, TimestampModel

# Define your models here:
# class Item(UUIDModel, TimestampModel):
#     name = models.CharField(max_length=255)
"""
    )

    # 4. admin.py
    (target_dir / "admin.py").write_text(
        """from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here:
# @admin.register(Item)
# class ItemAdmin(ModelAdmin):
#     list_display = ["id", "name", "created_at"]
"""
    )

    # 5. api.py
    (target_dir / "api.py").write_text(
        f"""from ninja import Router
from .schemas import MessageResponse

router = Router(tags=["{class_name}"])

@router.get("/health", response=MessageResponse)
def app_health(request):
    return {{"message": "{app_name} module operational"}}
"""
    )

    # 6. schemas.py
    (target_dir / "schemas.py").write_text(
        """from ninja import Schema
from pydantic import Field

class MessageResponse(Schema):
    message: str
"""
    )

    # 7. views.py
    (target_dir / "views.py").write_text(
        """from django.shortcuts import render
from django.http import HttpResponse

# neapolitan or standard views:
# from neapolitan.views import CRUDView
"""
    )

    # 8. urls.py
    (target_dir / "urls.py").write_text(
        f"""from django.urls import path
from . import views

app_name = "{app_name}"

urlpatterns = [
    # path("", views.index, name="index"),
]
"""
    )

    # 9. services.py
    (target_dir / "services.py").write_text(
        f"""\"\"\"Business logic and domain services for {app_name}.\"\"\"
"""
    )

    # 10. tasks.py
    (target_dir / "tasks.py").write_text(
        """from django_tasks import task, TaskContext
import structlog

logger = structlog.get_logger(__name__)

# @task(queue_name="default", priority=0)
# def sample_task(payload_id: str) -> dict:
#     logger.info("Executing task", payload_id=payload_id)
#     return {"status": "completed"}
"""
    )

    # 11. tests
    (tests_dir / "__init__.py").write_text("")
    (tests_dir / "factories.py").write_text(
        """import factory
from faker import Faker

fake = Faker()
"""
    )
    (tests_dir / "test_api.py").write_text(
        f"""import pytest
from django.test import Client

@pytest.mark.django_db
def test_{app_name}_health():
    client = Client()
    response = client.get("/api/v1/{app_name}/health")
    assert response.status_code == 200
    assert response.json()["message"] == "{app_name} module operational"
"""
    )

    print(f"{GREEN}✔ App '{app_name}' created successfully!{RESET}\n")
    print("Next steps:")
    print(
        f"  1. Add {BOLD}'apps.{app_name}'{RESET} to {BOLD}INSTALLED_APPS{RESET} in {BOLD}config/settings/base.py{RESET}"
    )
    print(f"  2. Mount the API router in {BOLD}config/api.py{RESET}:")
    print(f"     {BLUE}from apps.{app_name}.api import router as {app_name}_router{RESET}")
    print(f"     {BLUE}api.add_router('/{app_name}', {app_name}_router){RESET}")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.generators.app <app_name>")
        sys.exit(1)
    generate_app(sys.argv[1])
