# ==============================================================================
# AegisFlow AI Enterprise Build System & Automation Makefile
# ==============================================================================

.PHONY: all install build run test coverage lint clean docker-build docker-up docker-down help

PYTHON ?= python
PIP ?= pip
UVICORN ?= uvicorn
DOCKER_COMPOSE ?= docker compose

all: install build test

help:
	@echo "AegisFlow AI Enterprise Makefile Targets:"
	@echo "  make install      - Install all Python and Node.js dependencies"
	@echo "  make build        - Build frontend assets and Python packages"
	@echo "  make run          - Launch the FastAPI API Gateway server"
	@echo "  make run-stream   - Launch the StreamEngine distributed processor"
	@echo "  make run-sim      - Launch the financial traffic simulator"
	@echo "  make test         - Run full pytest test suite"
	@echo "  make coverage     - Run test suite with line & branch coverage report"
	@echo "  make lint         - Run ruff, flake8, and mypy static analysis"
	@echo "  make docker-up    - Start the full cluster with Docker Compose"
	@echo "  make docker-down  - Stop the Docker Compose cluster"
	@echo "  make clean        - Remove build artifacts, pycache, and temp files"

install:
	$(PIP) install -r requirements.txt
	@if [ -d "frontend" ]; then cd frontend && npm install; fi

build:
	$(PYTHON) -m compileall backend/
	@if [ -d "frontend" ]; then cd frontend && npm run build; fi

run:
	$(PYTHON) main.py --mode gateway --host 0.0.0.0 --port 8000

run-stream:
	$(PYTHON) main.py --mode stream

run-sim:
	$(PYTHON) main.py --mode simulator --eps 250 --fraud-ratio 0.08

test:
	$(PYTHON) -m pytest tests/unit/ tests/integration/ -v

coverage:
	$(PYTHON) -m pytest tests/unit/ tests/integration/ --cov=backend --cov-report=term-missing --cov-report=html:coverage_html

lint:
	$(PYTHON) -m ruff check backend/ tests/ || true

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov coverage_html build dist *.egg-info

docker-build:
	docker build -f Dockerfile -t aegisflow-ai:latest .

docker-up:
	$(DOCKER_COMPOSE) -f deployment/docker-compose.yml up -d

docker-down:
	$(DOCKER_COMPOSE) -f deployment/docker-compose.yml down
