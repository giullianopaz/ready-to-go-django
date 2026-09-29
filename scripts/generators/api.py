#!/usr/bin/env python3
"""
FastAPI-like REST API Generator using django-ninja and Pydantic V2.

Usage:
    python -m scripts.generators.api <app> <ModelName>
    make generate-api app=<app> model=<ModelName>
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


def generate_api(app_name: str, model_name: str) -> None:
    app_dir = APPS_DIR / app_name.lower().strip()
    if not app_dir.exists():
        print(f"Error: App '{app_name}' does not exist at {app_dir}")
        sys.exit(1)

    model_name = model_name.strip()
    var_name = model_name.lower()
    print(
        f"\n{BOLD}{BLUE}Scaffolding django-ninja API for:{RESET} {BOLD}{app_name}.{model_name}{RESET}"
    )

    # 1. Update schemas.py
    schemas_file = app_dir / "schemas.py"
    schemas_content = schemas_file.read_text() if schemas_file.exists() else ""
    if "from ninja import Schema" not in schemas_content:
        schemas_content = "from ninja import Schema\nfrom uuid import UUID\n\n" + schemas_content

    schema_code = f"""
class {model_name}In(Schema):
    name: str

class {model_name}Out(Schema):
    id: UUID
    name: str
"""
    schemas_file.write_text(schemas_content + schema_code)
    print(f"  {GREEN}✔{RESET} Pydantic schemas added to {schemas_file}")

    # 2. Update api.py
    api_file = app_dir / "api.py"
    api_content = api_file.read_text() if api_file.exists() else ""
    if f"from .models import {model_name}" not in api_content:
        api_content = (
            f"from django.shortcuts import get_object_or_404\n"
            f"from .models import {model_name}\n"
            f"from .schemas import {model_name}In, {model_name}Out\n" + api_content
        )

    endpoint_code = f"""
@router.get("/{var_name}s", response=list[{model_name}Out])
def list_{var_name}s(request):
    \"\"\"List all {model_name} records.\"\"\"
    return {model_name}.objects.all()

@router.get("/{var_name}s/{{{var_name}_id}}", response={model_name}Out)
def get_{var_name}(request, {var_name}_id: str):
    \"\"\"Retrieve a specific {model_name} by ID.\"\"\"
    return get_object_or_404({model_name}, id={var_name}_id)

@router.post("/{var_name}s", response={model_name}Out)
def create_{var_name}(request, payload: {model_name}In):
    \"\"\"Create a new {model_name}.\"\"\"
    instance = {model_name}.objects.create(**payload.dict())
    return instance

@router.delete("/{var_name}s/{{{var_name}_id}}")
def delete_{var_name}(request, {var_name}_id: str):
    \"\"\"Delete a {model_name} record.\"\"\"
    instance = get_object_or_404({model_name}, id={var_name}_id)
    instance.delete()
    return {{"success": True}}
"""
    api_file.write_text(api_content + endpoint_code)
    print(f"  {GREEN}✔{RESET} django-ninja endpoints added to {api_file}")

    print(f"\n{BOLD}{GREEN}API endpoints generated!{RESET}")
    print(f"Interactive documentation available at: {BLUE}http://localhost:8000/api/docs{RESET}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m scripts.generators.api <app> <ModelName>")
        sys.exit(1)
    generate_api(sys.argv[1], sys.argv[2])
