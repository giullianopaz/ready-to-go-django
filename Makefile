.PHONY: help setup-env run stop restart logs makemigrations migrate seed create-superuser setup-cache test test-unit test-integration coverage lint format typecheck quality shell dbshell generate-app generate-crud generate-api generate-task generate-openapi clean init

# Colors for help menu
BLUE := \033[36m
GREEN := \033[32m
RESET := \033[0m

help: ## Display this help screen
	@echo "$(BLUE)Available Makefile Targets:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$2}'

setup-env: ## First-time project setup (generates .env, installs deps via uv, sets up git hooks)
	@python3 scripts/setup_env.py

run: ## Launch complete local development environment with Docker Compose
	docker compose up --build

init: ## Initialize database (run migrations, seed data, create superuser) inside running Docker containers
	docker compose exec web python manage.py migrate
	docker compose exec web python manage.py createcachetable || true
	docker compose exec web python manage.py seed
	docker compose exec web python manage.py createsuperuser

stop: ## Stop all running Docker Compose services
	docker compose down

restart: ## Restart Docker Compose services in detached mode
	docker compose down && docker compose up --build -d

logs: ## Tail logs from Docker Compose services
	docker compose logs -f

makemigrations: ## Generate a new Django migration based on model changes
	docker compose exec web python manage.py makemigrations

migrate: ## Apply pending Django database migrations
	docker compose exec web python manage.py migrate

dbshell: ## Connect directly to the PostgreSQL database via psql
	docker compose exec db psql -U django -d django_db

seed: ## Seed database with default roles, permissions, and initial data
	docker compose exec web python manage.py seed

create-superuser: ## Create an administrative superuser account interactively
	docker compose exec web python manage.py createsuperuser

setup-cache: ## Ensure PostgreSQL unlogged cache table exists
	docker compose exec web python manage.py createcachetable

test: ## Execute complete test suite via pytest
	uv run pytest tests/ apps/ -v

test-unit: ## Execute unit test suite only
	uv run pytest tests/unit/ -v

test-integration: ## Execute integration test suite only
	uv run pytest tests/integration/ -v

coverage: ## Execute test suite with HTML coverage reporting
	uv run pytest --cov=apps --cov-report=html --cov-report=term-missing tests/ apps/

lint: ## Check code formatting and linting via ruff
	uv run ruff check .
	uv run ruff format --check .

format: ## Automatically fix linting and formatting errors via ruff
	uv run ruff check --fix .
	uv run ruff format .

typecheck: ## Run static type checking via pyright
	uv run pyright

quality: lint typecheck ## Run both linting and static type checking

shell: ## Open an interactive Django shell (shell_plus)
	docker compose exec web python manage.py shell_plus

generate-app: ## Scaffold a new Django app (usage: make generate-app name=products)
	@if [ -z "$(name)" ]; then echo "Error: Specify name, e.g. make generate-app name=products"; exit 1; fi
	uv run python -m scripts.generators.app $(name)

generate-crud: ## Scaffold full CRUD model, admin, view and urls (usage: make generate-crud app=products model=Product fields="name:str price:decimal")
	@if [ -z "$(app)" ] || [ -z "$(model)" ]; then echo "Error: Usage: make generate-crud app=products model=Product fields=\"name:str price:decimal\""; exit 1; fi
	uv run python -m scripts.generators.crud $(app) $(model) $(fields)

generate-api: ## Scaffold REST API endpoints with django-ninja (usage: make generate-api app=products model=Product)
	@if [ -z "$(app)" ] || [ -z "$(model)" ]; then echo "Error: Usage: make generate-api app=products model=Product"; exit 1; fi
	uv run python -m scripts.generators.api $(app) $(model)

generate-task: ## Scaffold a background task (usage: make generate-task app=products name=sync_inventory)
	@if [ -z "$(app)" ] || [ -z "$(name)" ]; then echo "Error: Usage: make generate-task app=products name=sync_inventory"; exit 1; fi
	uv run python -m scripts.generators.task $(app) $(name)

generate-openapi: ## Export OpenAPI JSON spec to disk for frontend SDK generators
	uv run python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development'); django.setup(); from config.api import api; import json; print(json.dumps(api.get_openapi_schema()))" > openapi.json
	@echo "$(BLUE)OpenAPI schema written to openapi.json$(RESET)"

clean: ## Remove Python build artifacts, caches, and coverage data
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ dist/ build/ *.egg-info openapi.json
