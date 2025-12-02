.PHONY: help up down build logs backend-shell frontend-shell db-shell migrate seed test lint clean

# Colors for terminal output
GREEN := \033[0;32m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "TaskFlow - Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Docker commands
up: ## Start all services
	docker compose up -d
	@echo "$(GREEN)Services started!$(NC)"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down: ## Stop all services
	docker compose down

build: ## Rebuild all containers
	docker compose build --no-cache

logs: ## Show logs from all services
	docker compose logs -f

logs-backend: ## Show backend logs
	docker compose logs -f backend

logs-frontend: ## Show frontend logs
	docker compose logs -f frontend

# Shell access
backend-shell: ## Open shell in backend container
	docker compose exec backend bash

frontend-shell: ## Open shell in frontend container
	docker compose exec frontend sh

db-shell: ## Open PostgreSQL shell
	docker compose exec db psql -U taskflow -d taskflow

# Database commands
migrate: ## Run database migrations
	docker compose exec backend alembic upgrade head

migrate-create: ## Create a new migration (usage: make migrate-create name="migration_name")
	docker compose exec backend alembic revision --autogenerate -m "$(name)"

seed: ## Seed the database with demo data
	docker compose exec backend python scripts/seed.py

# Testing
test: ## Run backend tests
	docker compose exec backend pytest -v

test-cov: ## Run backend tests with coverage
	docker compose exec backend pytest --cov=app --cov-report=term-missing

# Linting
lint: ## Run linters
	docker compose exec backend python -m flake8 app
	docker compose exec frontend npm run lint

lint-fix: ## Fix linting issues
	docker compose exec frontend npm run lint -- --fix

# Cleanup
clean: ## Remove all containers, volumes, and images
	docker compose down -v --rmi all
	@echo "$(GREEN)Cleanup complete!$(NC)"

# Development helpers
restart: ## Restart all services
	docker compose restart

restart-backend: ## Restart backend service
	docker compose restart backend

restart-frontend: ## Restart frontend service
	docker compose restart frontend

# Initial setup
setup: ## Initial project setup
	@echo "$(GREEN)Setting up TaskFlow...$(NC)"
	docker compose up -d --build
	@echo "Waiting for services to be ready..."
	sleep 10
	docker compose exec backend alembic upgrade head
	docker compose exec backend python scripts/seed.py
	@echo ""
	@echo "$(GREEN)Setup complete!$(NC)"
	@echo ""
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "Demo login:"
	@echo "  Email:    demo@taskflow.dev"
	@echo "  Password: demo1234"

