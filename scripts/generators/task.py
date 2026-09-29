#!/usr/bin/env python3
"""
Background Task Generator using django-tasks and PostgreSQL database queue.

Usage:
    python -m scripts.generators.task <app> <task_name>
    make generate-task app=<app> name=<task_name>
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


def generate_task(app_name: str, task_name: str) -> None:
    app_dir = APPS_DIR / app_name.lower().strip()
    if not app_dir.exists():
        print(f"Error: App '{app_name}' does not exist at {app_dir}")
        sys.exit(1)

    task_name = task_name.lower().strip()
    print(
        f"\n{BOLD}{BLUE}Scaffolding background task for:{RESET} {BOLD}{app_name}.{task_name}{RESET}"
    )

    tasks_file = app_dir / "tasks.py"
    tasks_content = tasks_file.read_text() if tasks_file.exists() else ""
    if "from django_tasks import task, TaskContext" not in tasks_content:
        tasks_content = (
            "import structlog\n"
            "from django_tasks import task, TaskContext\n\n"
            "logger = structlog.get_logger(__name__)\n\n" + tasks_content
        )

    task_code = f"""
@task(queue_name="default", priority=0, takes_context=True)
def {task_name}(context: TaskContext, record_id: str) -> dict:
    \"\"\"
    Background task {task_name} processed via PostgreSQL queue.
    \"\"\"
    logger.info("Executing background task", task="{task_name}", record_id=record_id, attempt=context.attempt)
    try:
        # Business logic goes here
        return {{"status": "completed", "record_id": record_id}}
    except Exception as exc:
        logger.error("Task failed", task="{task_name}", error=str(exc))
        raise
"""
    tasks_file.write_text(tasks_content + task_code)
    print(f"  {GREEN}✔{RESET} Background task {BOLD}{task_name}{RESET} added to {tasks_file}")
    print(f"\n{BOLD}{GREEN}Dispatch this task in views/services with:{RESET}")
    print(f"  {BLUE}from apps.{app_name}.tasks import {task_name}{RESET}")
    print(f"  {BLUE}{task_name}.enqueue(record_id){RESET}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m scripts.generators.task <app> <task_name>")
        sys.exit(1)
    generate_task(sys.argv[1], sys.argv[2])
