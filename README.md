# 🚀 Ready-to-Go Django

> **A State-of-the-Art Django 6.x Architecture for High-Velocity Startups**  
> *The Majestic Monolith in 2026: Convention Over Configuration, Consolidated PostgreSQL, and Pure Velocity.*

[![CI Pipeline](https://github.com/giullianopaz/ready-to-go-django/actions/workflows/ci.yml/badge.svg)](https://github.com/giullianopaz/ready-to-go-django/actions)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Django 6.x](https://img.shields.io/badge/django-6.1-green.svg)](https://www.djangoproject.com/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Architecture: Majestic Monolith](https://img.shields.io/badge/architecture-Majestic%20Monolith-orange.svg)](#)

---

## ⚡ Quickstart (Zero-Friction DX)

Clone the repository and run two commands:

```bash
# 1. First-time setup (generates .env with crypto secrets, installs dependencies via uv)
make setup-env

# 2. Launch the full environment (PostgreSQL 17, Web, Worker, and Mailpit)
make run
```

That's it! As soon as the containers start, open your browser:

- **Django Admin:** [http://localhost:8000/admin](http://localhost:8000/admin)  
  *Default Credentials:* Username: `admin` (or `admin@example.com`) / Password: `admin123`
- **Interactive REST API (Swagger UI):** [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- **Mailpit Web UI (Local Email Testing):** [http://localhost:8025](http://localhost:8025)
- **Application Landing Page:** [http://localhost:8000](http://localhost:8000)
- **Prometheus Metrics:** [http://localhost:8000/metrics](http://localhost:8000/metrics)
- **Health Probe:** [http://localhost:8000/up](http://localhost:8000/up)

---

## 🏛️ Architecture & Philosophy

The contemporary software landscape has moved past the premature complexity of microservices, distributed orchestration pipelines, and detached Single Page Applications (SPAs). **Ready-to-Go Django** brings the revered "Majestic Monolith" velocity to the Python ecosystem:

| Layer | Technology | Philosophy / Benefit |
|---|---|---|
| **ASGI Engine** | **Granian (Rust)** | Native HTTP/2, Rust event loop, +34% throughput over Uvicorn |
| **Admin Panel** | **django-unfold** | Tailwind CSS + HTMX modern dashboard out of the box |
| **Component UI** | **django-cotton** | HTML-like `<c-card>` component composition without React |
| **Interactivity** | **HTMX 4.0** | Asynchronous HTML-over-the-wire without frontend build steps |
| **CRUD Scaffolding**| **neapolitan** | Rails/Phoenix-like instant 5-endpoint CRUD generation |
| **REST APIs** | **django-ninja** | Pydantic V2 type hints with native OpenAPI documentation |
| **Consolidated DB**| **PostgreSQL 17** | Single service for relational data, UNLOGGED cache, and queues |
| **Cache Layer** | **PostgreSQL Cache** | `django_cache` table — zero Redis/Memcached dependencies |
| **Task Queue** | **django.tasks (DB)** | PostgreSQL task queue with worker process — zero Celery/RabbitMQ |
| **Package Manager**| **uv (Rust)** | Sub-second deterministic dependency resolution |
| **Observability** | **structlog + OpenTelemetry** | Structured JSON logging with trace and span IDs injected |
| **Local Email** | **Mailpit** | Visual SMTP interception with search and mobile previews |

---

## 🛠️ Rails/Phoenix-like Code Generators

Build comprehensive features in seconds with built-in code generators:

### 1. Scaffold a New Django App
```bash
make generate-app name=catalog
```
Generates a structured app under `apps/catalog/` containing models, admin, django-ninja router, Pydantic schemas, background tasks, domain services, URLs, and test suites.

### 2. Scaffold Full CRUD (Model + Admin + Views + URLs)
```bash
make generate-crud app=catalog model=Product fields="name:str price:decimal description:text in_stock:bool"
```
Instantly generates:
- Model subclassing `UUIDModel` and `TimestampModel`
- Unfold `ModelAdmin` with date range and field filters
- neapolitan `CRUDView` providing list, detail, create, edit, and delete
- Automatic URL routing

### 3. Scaffold django-ninja REST API
```bash
make generate-api app=catalog model=Product
```
Generates Pydantic `In`/`Out` schemas and REST endpoints automatically visible in Swagger UI at `/api/v1/docs`.

### 4. Scaffold Background Task
```bash
make generate-task app=catalog name=sync_inventory
```
Generates a background task in `apps/catalog/tasks.py` that executes via the PostgreSQL queue.

---

## 🤖 AI Agent & MCP Integration

Ready-to-Go Django is AI-native:
- **Model Context Protocol (MCP):** Endpoints `/api/v1/mcp/tools` and `/api/v1/mcp/tools/execute` expose application capabilities for tool-calling AI agents.
- **Pydantic V2 Schemas:** The exact same schemas validating incoming API requests can be supplied to `pydantic-ai` or LangChain without translation layers.
- **XSS & Prompt Injection Defense:** Input fields sanitized via `nh3` Rust library using `SanitizedStr` before reaching business logic or LLMs.

---

## 📋 Makefile Targets Reference

Run `make help` to inspect all 28 targets:

```
Available Makefile Targets:
  help                 Display this help screen
  setup-env            First-time project setup (generates .env, installs deps via uv, sets up git hooks)
  run                  Launch complete local development environment with Docker Compose
  init                 Initialize database (run migrations, seed data, create superuser) inside running Docker containers
  stop                 Stop all running Docker Compose services
  restart              Restart Docker Compose services in detached mode
  logs                 Tail logs from Docker Compose services
  makemigrations       Generate a new Django migration based on model changes
  migrate              Apply pending Django database migrations
  dbshell              Connect directly to the PostgreSQL database via psql
  seed                 Seed database with default roles, permissions, and initial data
  create-superuser     Create an administrative superuser account interactively
  setup-cache          Ensure PostgreSQL unlogged cache table exists
  test                 Execute complete test suite via pytest
  test-unit            Execute unit test suite only
  test-integration     Execute integration test suite only
  coverage             Execute test suite with HTML coverage reporting
  lint                 Check code formatting and linting via ruff
  format               Automatically fix linting and formatting errors via ruff
  typecheck            Run static type checking via pyright
  quality              Run both linting and static type checking
  shell                Open an interactive Django shell (shell_plus)
  generate-app         Scaffold a new Django app (usage: make generate-app name=products)
  generate-crud        Scaffold full CRUD model, admin, view and urls
  generate-api         Scaffold REST API endpoints with django-ninja
  generate-task        Scaffold a background task
  generate-openapi     Export OpenAPI JSON spec to disk for frontend SDK generators
  clean                Remove Python build artifacts, caches, and coverage data
```

---

## 🧪 Testing & Quality Assurance

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Generate HTML test coverage report
make coverage

# Code quality checks (linter + typechecker)
make quality
```

---

## 🔒 Security Hardening

- **Argon2 Password Hashing:** Modern memory-hard hashing algorithm (`django.contrib.auth.hashers.Argon2PasswordHasher`).
- **nh3 HTML Sanitization:** Memory-safe Rust scrubbing against persistent XSS and prompt injection.
- **Double-Submit CSRF Defense:** Native Django CSRF token validation on all state-mutating requests.
- **HTTP Security Headers:** HSTS, X-Content-Type-Options, X-Frame-Options, and Content Security Policy (`django-csp`).
- **Parameterized Queries:** Django ORM ensures complete immunity against SQL injection.
