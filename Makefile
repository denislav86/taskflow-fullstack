# =============================================================================
# TaskFlow - Makefile
# =============================================================================
# Development commands for managing the TaskFlow application
#
# Usage: make <target>
# =============================================================================

.PHONY: help up down build logs backend-shell frontend-shell db-shell \
        migrate seed test lint clean setup restart install-deps

# Colors for terminal output
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m

# Default target
.DEFAULT_GOAL := help

# =============================================================================
# Help
# =============================================================================
help: ## Show this help message
	@echo ""
	@echo "$(BLUE)TaskFlow - Development Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Docker Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*Docker.*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-18s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Development Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*Dev.*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-18s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Database Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*DB.*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-18s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Testing Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*Test.*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-18s$(NC) %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# Docker Commands
# =============================================================================
up: ## [Docker] Start all services in foreground
	docker compose up

up-d: ## [Docker] Start all services in background
	docker compose up -d
	@echo ""
	@echo "$(GREEN)✅ Services started!$(NC)"
	@echo ""
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend:  http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"
	@echo ""

down: ## [Docker] Stop all services
	docker compose down

build: ## [Docker] Rebuild all containers (no cache)
	docker compose build --no-cache

build-cached: ## [Docker] Rebuild all containers (with cache)
	docker compose build

logs: ## [Docker] Show logs from all services
	docker compose logs -f

logs-backend: ## [Docker] Show backend logs only
	docker compose logs -f backend

logs-frontend: ## [Docker] Show frontend logs only
	docker compose logs -f frontend

restart: ## [Docker] Restart all services
	docker compose restart

restart-backend: ## [Docker] Restart backend service
	docker compose restart backend

restart-frontend: ## [Docker] Restart frontend service
	docker compose restart frontend

ps: ## [Docker] Show running containers
	docker compose ps

# =============================================================================
# Shell Access
# =============================================================================
backend-shell: ## [Dev] Open shell in backend container
	docker compose exec backend bash

frontend-shell: ## [Dev] Open shell in frontend container
	docker compose exec frontend sh

db-shell: ## [DB] Open PostgreSQL shell
	docker compose exec db psql -U taskflow -d taskflow

# =============================================================================
# Database Commands
# =============================================================================
migrate: ## [DB] Run database migrations
	docker compose exec backend alembic upgrade head

migrate-down: ## [DB] Rollback last migration
	docker compose exec backend alembic downgrade -1

migrate-create: ## [DB] Create new migration (usage: make migrate-create name="description")
	docker compose exec backend alembic revision --autogenerate -m "$(name)"

migrate-history: ## [DB] Show migration history
	docker compose exec backend alembic history

seed: ## [DB] Seed database with demo data
	docker compose exec backend python scripts/seed.py

db-reset: ## [DB] Reset database (drop and recreate)
	docker compose exec db psql -U taskflow -c "DROP DATABASE IF EXISTS taskflow;"
	docker compose exec db psql -U taskflow -c "CREATE DATABASE taskflow;"
	docker compose exec backend alembic upgrade head
	@echo "$(GREEN)✅ Database reset complete!$(NC)"

# =============================================================================
# Testing Commands
# =============================================================================
test: ## [Test] Run backend tests
	docker compose exec backend pytest -v

test-cov: ## [Test] Run backend tests with coverage
	docker compose exec backend pytest --cov=app --cov-report=term-missing --cov-report=html

test-watch: ## [Test] Run backend tests in watch mode
	docker compose exec backend pytest-watch

# =============================================================================
# Linting Commands
# =============================================================================
lint: ## [Dev] Run all linters
	@echo "$(BLUE)Running backend linting...$(NC)"
	docker compose exec backend flake8 app
	@echo "$(BLUE)Running frontend linting...$(NC)"
	docker compose exec frontend pnpm lint
	@echo "$(GREEN)✅ Linting complete!$(NC)"

lint-backend: ## [Dev] Run backend linter
	docker compose exec backend flake8 app

lint-frontend: ## [Dev] Run frontend linter
	docker compose exec frontend pnpm lint

lint-fix: ## [Dev] Fix frontend linting issues
	docker compose exec frontend pnpm lint --fix

typecheck: ## [Dev] Run TypeScript type check
	docker compose exec frontend pnpm exec tsc --noEmit

# =============================================================================
# Dependency Management
# =============================================================================
install-deps: ## [Dev] Install/update dependencies in containers
	@echo "$(BLUE)Installing backend dependencies...$(NC)"
	docker compose exec backend pip install -r requirements.txt
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	docker compose exec frontend pnpm install
	@echo "$(GREEN)✅ Dependencies installed!$(NC)"

# =============================================================================
# Cleanup Commands
# =============================================================================
clean: ## [Docker] Remove containers, volumes, and images
	docker compose down -v --rmi all --remove-orphans
	@echo "$(GREEN)✅ Cleanup complete!$(NC)"

clean-volumes: ## [Docker] Remove only volumes (keeps images)
	docker compose down -v
	@echo "$(GREEN)✅ Volumes removed!$(NC)"

prune: ## [Docker] Remove all unused Docker resources
	docker system prune -af --volumes
	@echo "$(GREEN)✅ Docker pruned!$(NC)"

# =============================================================================
# Setup Commands
# =============================================================================
setup: ## [Dev] Initial project setup (builds, migrates, seeds)
	@echo "$(BLUE)🚀 Setting up TaskFlow...$(NC)"
	@echo ""
	docker compose up -d --build
	@echo ""
	@echo "$(BLUE)⏳ Waiting for services to be ready...$(NC)"
	@sleep 15
	@echo ""
	@echo "$(BLUE)📦 Running database migrations...$(NC)"
	docker compose exec backend alembic upgrade head
	@echo ""
	@echo "$(BLUE)🌱 Seeding demo data...$(NC)"
	docker compose exec backend python scripts/seed.py
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✅ Setup complete!$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "  $(BLUE)Frontend:$(NC)  http://localhost:3000"
	@echo "  $(BLUE)Backend:$(NC)   http://localhost:8000"
	@echo "  $(BLUE)API Docs:$(NC)  http://localhost:8000/docs"
	@echo ""
	@echo "  $(YELLOW)Demo Login:$(NC)"
	@echo "    Email:    demo@taskflow.dev"
	@echo "    Password: demo1234"
	@echo ""

# =============================================================================
# Production Commands
# =============================================================================
prod-build: ## [Docker] Build production images
	docker compose -f docker-compose.prod.yml build

prod-up: ## [Docker] Start production services
	docker compose -f docker-compose.prod.yml up -d

prod-down: ## [Docker] Stop production services
	docker compose -f docker-compose.prod.yml down
