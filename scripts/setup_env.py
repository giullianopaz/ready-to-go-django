#!/usr/bin/env python3
"""
One-command project setup for Ready-to-Go Django.

Usage:
    python3 scripts/setup_env.py
    # or
    make setup-env

Steps performed:
  1. Generate .env from .env.example with cryptographically secure secrets
  2. Install Python dependencies via uv
  3. Ensure uv.lock is present
  4. Install pre-commit hooks
  5. Print next-step instructions
"""

from __future__ import annotations

import secrets
import shutil
import subprocess
import sys
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_EXAMPLE = ROOT_DIR / ".env.example"
ENV_FILE = ROOT_DIR / ".env"
UV_LOCK = ROOT_DIR / "uv.lock"

# Colours (ANSI)
BLUE = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"


def info(msg: str) -> None:
    print(f"  {BLUE}▸{RESET} {msg}")


def success(msg: str) -> None:
    print(f"  {GREEN}✔{RESET} {msg}")


def warn(msg: str) -> None:
    print(f"  {YELLOW}⚠{RESET} {msg}")


def error(msg: str) -> None:
    print(f"  {RED}✖{RESET} {msg}")


def header(msg: str) -> None:
    print(f"\n{BOLD}{BLUE}{'─' * 60}{RESET}")
    print(f"  {BOLD}{msg}{RESET}")
    print(f"{BOLD}{BLUE}{'─' * 60}{RESET}\n")


def generate_secret(length: int = 64) -> str:
    """Generate a cryptographically secure URL-safe token."""
    return secrets.token_urlsafe(length)


def create_env_file() -> None:
    """Create .env from .env.example, injecting real secrets."""
    if ENV_FILE.exists():
        warn(f".env already exists — skipping ({ENV_FILE})")
        return

    if not ENV_EXAMPLE.exists():
        error(f".env.example not found at {ENV_EXAMPLE}")
        sys.exit(1)

    info("Generating .env from .env.example with secure secrets...")

    content = ENV_EXAMPLE.read_text()

    # Generate secrets for Django, JWT, and Postgres
    django_secret = generate_secret(50)
    jwt_secret = generate_secret(50)
    postgres_password = secrets.token_hex(16)

    content = content.replace("change_this_to_a_secure_random_key_in_production", django_secret)
    content = content.replace("change_this_jwt_secret_key_in_production", jwt_secret)
    content = content.replace("change_this_postgres_password_in_production", postgres_password)

    ENV_FILE.write_text(content)
    success(f".env created at {ENV_FILE}")


def install_dependencies() -> None:
    """Install Python dependencies via uv."""
    uv = shutil.which("uv")
    if not uv:
        error("'uv' is not installed. Please install uv (https://docs.astral.sh/uv/)")
        sys.exit(1)

    info("Installing Python dependencies (uv sync --all-extras)...")
    result = subprocess.run(
        [uv, "sync", "--all-extras"],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        error("uv sync failed:")
        print(result.stderr)
        sys.exit(1)

    success("Dependencies installed successfully.")


def ensure_lockfile() -> None:
    """Generate uv.lock if missing."""
    if UV_LOCK.exists():
        success("uv.lock already present.")
        return

    uv = shutil.which("uv")
    if not uv:
        return

    info("Generating uv.lock...")
    result = subprocess.run(
        [uv, "lock"],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        error("uv lock failed:")
        print(result.stderr)
        sys.exit(1)

    success("uv.lock generated.")


def setup_pre_commit() -> None:
    """Install git pre-commit hooks."""
    uv = shutil.which("uv")
    if uv:
        result = subprocess.run(
            [uv, "run", "pre-commit", "install"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            success("Pre-commit hooks installed.")
            return

    warn("Skipping pre-commit hook installation (optional).")


def main() -> None:
    header("🚀 Ready-to-Go Django — Project Setup")

    create_env_file()
    install_dependencies()
    ensure_lockfile()
    setup_pre_commit()

    header("✅ Setup Complete!")
    print("  Next steps:\n")
    print(f"    {GREEN}1.{RESET} Start the stack:      {BOLD}make run{RESET}")
    print(f"    {GREEN}2.{RESET} Open Django Admin:    {BLUE}http://localhost:8000/admin{RESET}")
    print(
        f"       Default Login:        Username: {BOLD}admin{RESET} (or admin@example.com) / Password: {BOLD}admin123{RESET}"
    )
    print()
    print("  Available Services:")
    print(f"    • Django Admin:      {BLUE}http://localhost:8000/admin{RESET}")
    print(f"    • Interactive API:   {BLUE}http://localhost:8000/api/docs{RESET}")
    print(f"    • Mailpit Web UI:    {BLUE}http://localhost:8025{RESET}")
    print(f"    • Health Probe:      {BLUE}http://localhost:8000/up{RESET}")
    print(f"    • Prometheus Metrics:{BLUE}http://localhost:8000/metrics{RESET}")
    print()


if __name__ == "__main__":
    main()
