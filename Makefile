SERVER_NAME ?= notes_sync
DOCS_SERVER_NAME ?= $(SERVER_NAME)/docs

PROJECT_NAMESPACE ?= eoan-ermine
REGISTRY_NAME ?= ghcr.io

SERVER_IMAGE ?= $(REGISTRY_NAME)/$(PROJECT_NAMESPACE)/$(SERVER_NAME)
DOCS_SERVER_IMAGE ?= $(REGISTRY_NAME)/$(PROJECT_NAMESPACE)/$(DOCS_SERVER_NAME)

TEST = poetry run python3 -m pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = notes_sync

all:
	@echo "make shell\t\t — activate shell"
	@echo "make format\t\t — reformat code with isort and black"

shell:
	poetry shell

lint:
	poetry run ruff check $(CODE)

format:
	poetry run ruff format $(CODE)

requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

openapi:
	poetry --version

run:
	poetry run python3 -m $(CODE)

images:
	docker build -f Dockerfile --target producer -t notes_sync_server .
	docker build -f Dockerfile --target health_check_consumer -t notes_sync_health_check_consumer .
	docker build -f Dockerfile --target logsequence_consumer -t notes_sync_logsequence_consumer .

up:
	docker compose -f docker-compose.yml up --detach --remove-orphans

down:
	docker compose down

open_db:
	docker exec -it notes_sync_db psql -U ${DB_USER} -W ${DB_NAME}

migrate:
	poetry run alembic --config notes_sync/database/alembic.ini upgrade head

revision:
	poetry run alembic --config notes_sync/database/alembic.ini revision --autogenerate

clean_db: down
	docker volume rm $(shell docker volume ls --quiet)

test: db
	$(TEST)

test_cov: db
	$(TEST) --cov=notes_sync