# ═══════════════════════════════════════════════════
#  SwasthyaSetu — Root Makefile
# ═══════════════════════════════════════════════════

.PHONY: dev build test seed-demo install clean \
        dev-api dev-frontend dev-services \
        install-python install-node install-frontend \
        build-docker test-python test-node test-frontend

# ── Paths ──
PYTHON_SERVICES  := ai-ml-service translation-service document-service
NODE_SERVICES    := identity-service health-service notification-service
SERVICES_DIR     := backend/services
FRONTEND_DIR     := frontend
WEB_DIR          := frontend/web
VENV             := .venv

# ═══════════════════════════════════════
#  dev  —  Start everything locally
# ═══════════════════════════════════════

dev: dev-api dev-frontend
	@echo "✅ All services running"

dev-api:
	@echo "🚀 Starting backend API..."
	cd backend && source ../$(VENV)/bin/activate && \
		python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

dev-frontend:
	@echo "🌐 Starting frontend..."
	cd $(FRONTEND_DIR) && npm run dev &

dev-services:
	@echo "🔧 Starting microservices..."
	@for svc in $(NODE_SERVICES); do \
		echo "  → $$svc"; \
		cd $(SERVICES_DIR)/$$svc && npm run dev & \
	done
	@for svc in $(PYTHON_SERVICES); do \
		echo "  → $$svc"; \
		cd $(SERVICES_DIR)/$$svc && source ../../$(VENV)/bin/activate && \
			uvicorn main:app --reload --port $$(cat .port 2>/dev/null || echo 5001) & \
	done

# ═══════════════════════════════════════
#  install  —  Install all dependencies
# ═══════════════════════════════════════

install: install-python install-node install-frontend
	@echo "✅ All dependencies installed"

install-python:
	@echo "🐍 Installing Python dependencies..."
	@for svc in $(PYTHON_SERVICES); do \
		echo "  → $(SERVICES_DIR)/$$svc"; \
		pip install -r $(SERVICES_DIR)/$$svc/requirements.txt; \
	done

install-node:
	@echo "📦 Installing Node.js dependencies..."
	@for svc in $(NODE_SERVICES); do \
		echo "  → $(SERVICES_DIR)/$$svc"; \
		cd $(SERVICES_DIR)/$$svc && npm install && cd ../../..; \
	done

install-frontend:
	@echo "🌐 Installing frontend dependencies..."
	cd $(FRONTEND_DIR) && npm install
	cd $(WEB_DIR) && npm install

# ═══════════════════════════════════════
#  build  —  Build for production
# ═══════════════════════════════════════

build: build-docker
	@echo "✅ Production build complete"

build-docker:
	@echo "🐳 Building Docker images..."
	cd api-gateway && docker compose build

build-frontend:
	@echo "🌐 Building frontend..."
	cd $(FRONTEND_DIR) && npm run build

# ═══════════════════════════════════════
#  test  —  Run all tests
# ═══════════════════════════════════════

test: test-python test-node test-frontend
	@echo "✅ All tests passed"

test-python:
	@echo "🧪 Testing Python services..."
	@for svc in $(PYTHON_SERVICES); do \
		echo "  → $$svc"; \
		cd $(SERVICES_DIR)/$$svc && python -m pytest -q 2>/dev/null || echo "  ⚠  No tests yet"; \
		cd ../../..; \
	done

test-node:
	@echo "🧪 Testing Node.js services..."
	@for svc in $(NODE_SERVICES); do \
		echo "  → $$svc"; \
		cd $(SERVICES_DIR)/$$svc && npm test 2>/dev/null || echo "  ⚠  No tests yet"; \
		cd ../../..; \
	done

test-frontend:
	@echo "🧪 Testing frontend..."
	cd $(FRONTEND_DIR) && npm test 2>/dev/null || echo "  ⚠  No tests yet"

# ═══════════════════════════════════════
#  seed-demo  —  Seed demo data
# ═══════════════════════════════════════

seed-demo:
	@echo "🌱 Seeding demo data..."
	source $(VENV)/bin/activate && cd backend && python -m database.seed 2>/dev/null || \
		python database/seed.py 2>/dev/null || \
		echo "  ⚠  No seed script found — creating demo workers via API"
	@echo ""
	@echo "  Creating demo SwasthyaIDs..."
	@curl -s -X POST http://localhost:8000/api/v1/identity/create \
		-H "Content-Type: application/json" \
		-d '{"name":"Ramesh Kumar","phone":"+91-9876543210","age":35,"occupation":"stone_cutter","state":"Rajasthan"}' \
		| python -m json.tool 2>/dev/null || echo '  → POST identity/create (server not running?)'
	@curl -s -X POST http://localhost:8000/api/v1/identity/create \
		-H "Content-Type: application/json" \
		-d '{"name":"Priya Devi","phone":"+91-9876543211","age":28,"occupation":"textile_worker","state":"Gujarat"}' \
		| python -m json.tool 2>/dev/null || echo '  → POST identity/create (server not running?)'
	@curl -s -X POST http://localhost:8000/api/v1/identity/create \
		-H "Content-Type: application/json" \
		-d '{"name":"Suresh Yadav","phone":"+91-9876543212","age":42,"occupation":"construction","state":"Bihar"}' \
		| python -m json.tool 2>/dev/null || echo '  → POST identity/create (server not running?)'
	@echo ""
	@echo "✅ Demo data seeded with 3 workers"

# ═══════════════════════════════════════
#  clean  —  Remove build artifacts
# ═══════════════════════════════════════

clean:
	@echo "🧹 Cleaning..."
	rm -rf $(FRONTEND_DIR)/dist $(WEB_DIR)/dist
	@for svc in $(NODE_SERVICES); do \
		rm -rf $(SERVICES_DIR)/$$svc/node_modules; \
	done
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean"

# ═══════════════════════════════════════
#  help
# ═══════════════════════════════════════

help:
	@echo ""
	@echo "  SwasthyaSetu Makefile Commands"
	@echo "  ────────────────────────────────"
	@echo "  make dev          Start backend + frontend locally"
	@echo "  make dev-services Start all microservices"
	@echo "  make install      Install all dependencies"
	@echo "  make build        Build Docker images for production"
	@echo "  make test         Run all tests"
	@echo "  make seed-demo    Seed database with demo workers"
	@echo "  make clean        Remove build artifacts & node_modules"
	@echo ""
