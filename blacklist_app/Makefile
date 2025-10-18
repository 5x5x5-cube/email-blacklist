# Makefile for blacklist_app

# All environment variables are expected to be set in .env file
# See .env.example for required variables

.PHONY: setup install run test clean docker-build docker-run docker-push

setup:
	@echo "Setting up the project..."
	@pip install poetry
	@poetry install

install:
	@echo "Installing dependencies..."
	@poetry install

run:
	@echo "Running the application..."
	@set -a && source .env && set +a && poetry run flask --app src.main:app run --reload --host 0.0.0.0 --port 5001

test:
	@echo "Running tests..."
	@set -a && source .env.test && set +a && poetry run pytest

test-unit:
	@echo "Running unit tests..."
	@set -a && source .env.test && set +a && poetry run pytest tests/unit

test-cov:
	@echo "Running tests with coverage..."
	@set -a && source .env.test && set +a && poetry run pytest --cov=src tests/ --cov-report=term-missing --cov-report=xml

clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__
	@rm -rf .pytest_cache
	@rm -rf .coverage

docker-build:
	@echo "Building Docker image with platform linux/amd64..."
	$(eval IMAGE_NAME=$(shell grep IMAGE_NAME .env | cut -d '=' -f2))
	$(eval IMAGE_TAG=$(shell grep IMAGE_TAG .env | cut -d '=' -f2))
	@echo "Building image: $(IMAGE_NAME):$(IMAGE_TAG)"
	@docker build --platform linux/amd64 -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-run:
	@echo "Running Docker container..."
	@eval $$(cat .env | sed 's/^/export /' | sed 's/#.*//')
	@docker run -p 5000:5000 --env-file .env $${IMAGE_NAME}:$${IMAGE_TAG}

docker-compose-up:
	@echo "Starting Docker Compose services..."
	@docker compose up -d

docker-compose-build:
	@echo "Starting Docker Compose services with rebuild (platform: linux/amd64)..."
	@DOCKER_DEFAULT_PLATFORM=linux/amd64 docker compose up -d --build

docker-compose-down:
	@echo "Stopping Docker Compose services..."
	@docker compose down