#!/usr/bin/env python3
"""
Rails-like CRUD Generator using neapolitan & django-unfold.

Usage:
    python -m scripts.generators.crud <app> <ModelName> [field:type ...]
    make generate-crud app=<app> model=<ModelName> fields="title:str price:decimal"

Supported field types:
    str (CharField)
    text (TextField)
    int (IntegerField)
    decimal (DecimalField)
    bool (BooleanField)
    email (EmailField)
    date (DateField)
    datetime (DateTimeField)
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

FIELD_MAP = {
    "str": "models.CharField(max_length=255)",
    "text": "models.TextField(blank=True, default='')",
    "int": "models.IntegerField(default=0)",
    "decimal": "models.DecimalField(max_digits=12, decimal_places=2, default=0.00)",
    "bool": "models.BooleanField(default=False)",
    "email": "models.EmailField(blank=True, default='')",
    "date": "models.DateField(null=True, blank=True)",
    "datetime": "models.DateTimeField(null=True, blank=True)",
}


def generate_crud(app_name: str, model_name: str, fields: list[str]) -> None:
    app_dir = APPS_DIR / app_name.lower().strip()
    if not app_dir.exists():
        print(f"Error: App '{app_name}' does not exist at {app_dir}")
        print("Create it first with: make generate-app name=" + app_name)
        sys.exit(1)

    model_name = model_name.strip()
    print(f"\n{BOLD}{BLUE}Scaffolding CRUD for:{RESET} {BOLD}{app_name}.{model_name}{RESET}")

    field_defs = []
    field_names = []

    for f in fields:
        if ":" in f:
            name, ftype = f.split(":", 1)
        else:
            name, ftype = f, "str"
        name = name.strip()
        ftype = ftype.strip().lower()
        field_names.append(name)
        django_type = FIELD_MAP.get(ftype, "models.CharField(max_length=255)")
        field_defs.append(f"    {name} = {django_type}")

    if not field_defs:
        field_names = ["name"]
        field_defs = ["    name = models.CharField(max_length=255)"]

    fields_code = "\n".join(field_defs)
    field_list_repr = str(field_names)

    # 1. Update models.py
    models_file = app_dir / "models.py"
    models_content = models_file.read_text() if models_file.exists() else ""
    if "from apps.core.models import UUIDModel, TimestampModel" not in models_content:
        models_content = (
            "from django.db import models\n"
            "from apps.core.models import UUIDModel, TimestampModel\n\n" + models_content
        )

    model_class_code = f"""
class {model_name}(UUIDModel, TimestampModel):
{fields_code}

    class Meta:
        verbose_name = "{model_name}"
        verbose_name_plural = "{model_name}s"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{model_name}({{self.id}})"
"""
    models_file.write_text(models_content + model_class_code)
    print(f"  {GREEN}✔{RESET} Model {BOLD}{model_name}{RESET} added to {models_file}")

    # 2. Update admin.py
    admin_file = app_dir / "admin.py"
    admin_content = admin_file.read_text() if admin_file.exists() else ""
    if "from unfold.admin import ModelAdmin" not in admin_content:
        admin_content = (
            "from django.contrib import admin\n"
            "from unfold.admin import ModelAdmin\n"
            f"from .models import {model_name}\n\n" + admin_content
        )
    else:
        admin_content = f"from .models import {model_name}\n" + admin_content

    admin_code = f"""
@admin.register({model_name})
class {model_name}Admin(ModelAdmin):
    list_display = ["id"] + {field_list_repr} + ["created_at"]
    search_fields = {field_list_repr}
    list_filter_submit = True
"""
    admin_file.write_text(admin_content + admin_code)
    print(f"  {GREEN}✔{RESET} Admin dashboard for {BOLD}{model_name}{RESET} added to {admin_file}")

    # 3. Update views.py
    views_file = app_dir / "views.py"
    views_content = views_file.read_text() if views_file.exists() else ""
    if "from neapolitan.views import CRUDView" not in views_content:
        views_content = (
            "from neapolitan.views import CRUDView\n"
            f"from .models import {model_name}\n\n" + views_content
        )
    else:
        views_content = f"from .models import {model_name}\n" + views_content

    crud_view_code = f"""
class {model_name}View(CRUDView):
    model = {model_name}
    fields = {field_list_repr}
"""
    views_file.write_text(views_content + crud_view_code)
    print(
        f"  {GREEN}✔{RESET} neapolitan CRUDView for {BOLD}{model_name}{RESET} added to {views_file}"
    )

    # 4. Update urls.py
    urls_file = app_dir / "urls.py"
    urls_content = urls_file.read_text() if urls_file.exists() else ""
    if f"from .views import {model_name}View" not in urls_content:
        urls_content = f"from .views import {model_name}View\n" + urls_content
    if "urlpatterns = [" in urls_content:
        urls_content = urls_content.replace(
            "urlpatterns = [", f"urlpatterns = [\n    *{model_name}View.get_urls(),"
        )
    else:
        urls_content += f"\nurlpatterns = [\n    *{model_name}View.get_urls(),\n]\n"
    urls_file.write_text(urls_content)
    print(f"  {GREEN}✔{RESET} Endpoints for {BOLD}{model_name}{RESET} registered in {urls_file}")

    print(f"\n{BOLD}{GREEN}CRUD generation complete!{RESET}")
    print(f"Now run:\n  {BOLD}make makemigrations{RESET}\n  {BOLD}make migrate{RESET}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m scripts.generators.crud <app> <ModelName> [field:type ...]")
        sys.exit(1)
    app = sys.argv[1]
    model = sys.argv[2]
    flds = sys.argv[3:]
    generate_crud(app, model, flds)
