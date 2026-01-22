.PHONY: help dev-up dev-down dev-logs dev-shell prod-up prod-down prod-logs migrate migrate-create migrate-upgrade migrate-downgrade test clean

# Default target
help:
	@echo "Face Recognition Service - Makefile Commands"
	@echo ""
	@echo "Development:"
	@echo "  make dev-up          - Start development environment (all services)"
	@echo "  make dev-up-backend - Start only backend services (for local frontend dev)"
	@echo "  make dev-down        - Stop development environment"
	@echo "  make dev-logs        - View development logs"
	@echo "  make dev-shell       - Open shell in backend container"
	@echo ""
	@echo "Production:"
	@echo "  make prod-up         - Start production environment"
	@echo "  make prod-down       - Stop production environment"
	@echo "  make prod-logs       - View production logs"
	@echo ""
	@echo "Database Migrations:"
	@echo "  make migrate         - Run all pending migrations"
	@echo "  make migrate-create  - Create a new migration (use MESSAGE='description')"
	@echo "  make migrate-upgrade - Upgrade database to head"
	@echo "  make migrate-downgrade - Downgrade database by one revision"
	@echo ""
	@echo "Other:"
	@echo "  make test            - Run tests"
	@echo "  make clean           - Clean up containers and volumes"

# Development environment
dev-up:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 5
	@echo "Development environment is running!"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

dev-up-backend:
	@echo "Starting backend services (PostgreSQL + Backend)..."
	docker-compose up -d postgres backend
	@echo "Waiting for services to be ready..."
	@sleep 5
	@echo "Backend services are running!"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "To run frontend locally:"
	@echo "  cd apps/frontend && npm install && npm run dev"

dev-down:
	@echo "Stopping development environment..."
	docker-compose down

dev-logs:
	docker-compose logs -f

dev-shell:
	docker-compose exec face_recognition_backend /bin/bash

# Production environment
prod-up:
	@echo "Starting production environment..."
	@if [ ! -f .env.prod ]; then \
		echo "Error: .env.prod file not found!"; \
		echo "Please create .env.prod with required environment variables."; \
		exit 1; \
	fi
	docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
	@echo "Waiting for services to be ready..."
	@sleep 5
	@echo "Production environment is running!"

prod-down:
	@echo "Stopping production environment..."
	docker-compose -f docker-compose.prod.yml --env-file .env.prod down

prod-logs:
	docker-compose -f docker-compose.prod.yml --env-file .env.prod logs -f

# Database migrations
migrate:
	@echo "Running database migrations..."
	docker-compose exec face_recognition_backend alembic upgrade head

migrate-create:
	@if [ -z "$(MESSAGE)" ]; then \
		echo "Error: MESSAGE is required. Usage: make migrate-create MESSAGE='description'"; \
		exit 1; \
	fi
	@echo "Creating new migration: $(MESSAGE)"
	docker-compose exec face_recognition_backend alembic revision --autogenerate -m "$(MESSAGE)"

migrate-upgrade:
	@echo "Upgrading database to head..."
	docker-compose exec face_recognition_backend alembic upgrade head

migrate-downgrade:
	@echo "Downgrading database by one revision..."
	docker-compose exec face_recognition_backend alembic downgrade -1

# Local migration commands (without docker)
migrate-local:
	cd apps/backend && alembic upgrade head

migrate-create-local:
	@if [ -z "$(MESSAGE)" ]; then \
		echo "Error: MESSAGE is required. Usage: make migrate-create-local MESSAGE='description'"; \
		exit 1; \
	fi
	cd apps/backend && alembic revision --autogenerate -m "$(MESSAGE)"

# Testing
test:
	@echo "Running tests..."
	docker-compose exec face_recognition_backend pytest

# Cleanup
clean:
	@echo "Cleaning up containers and volumes..."
	docker-compose down -v
	@echo "Cleanup complete!"

clean-prod:
	@echo "Cleaning up production containers and volumes..."
	docker-compose -f docker-compose.prod.yml --env-file .env.prod down -v
	@echo "Production cleanup complete!"

