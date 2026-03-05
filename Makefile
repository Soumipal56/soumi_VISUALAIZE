.PHONY: help dev dev-build prod prod-build down logs \
        backend-install backend-run backend-test backend-lint \
        frontend-install frontend-run frontend-build frontend-lint

# ─── Default target ─────────────────────────────────────────────────────────
help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} \
	/^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# ─── Docker Compose ──────────────────────────────────────────────────────────
dev-build: ## Build images for local development
	docker compose build

dev: ## Start all services in development mode (build if needed)
	docker compose up --build

prod-build: ## Build images for production
	docker compose -f docker-compose.yml -f docker-compose.prod.yml build

prod: ## Start all services in production mode
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down: ## Stop and remove all containers
	docker compose down

logs: ## Tail logs for all services
	docker compose logs -f

logs-backend: ## Tail backend logs
	docker compose logs -f backend

logs-frontend: ## Tail frontend logs
	docker compose logs -f frontend

# ─── Backend (local) ─────────────────────────────────────────────────────────
backend-install: ## Install Python dependencies
	cd backend && pip install -r requirements.txt

backend-run: ## Run backend dev server locally
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

backend-test: ## Run backend unit tests
	cd backend && pytest test_server.py -v

backend-lint: ## Lint backend Python code
	cd backend && flake8 main.py --max-line-length=120

# ─── Frontend (local) ────────────────────────────────────────────────────────
frontend-install: ## Install Node.js dependencies
	cd frontend && npm ci

frontend-run: ## Run frontend dev server locally
	cd frontend && npm run dev

frontend-build: ## Build frontend for production
	cd frontend && npm run build

frontend-lint: ## Lint frontend TypeScript/React code
	cd frontend && npm run lint

frontend-typecheck: ## Type-check frontend TypeScript
	cd frontend && npx tsc --noEmit
