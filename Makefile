SERVER_NAME ?= notes_sync
DOCS_SERVER_NAME ?= $(SERVER_NAME)/docs

PROJECT_NAMESPACE ?= eoan-ermine
REGISTRY_NAME ?= ghcr.io

SERVER_IMAGE ?= $(REGISTRY_NAME)/$(PROJECT_NAMESPACE)/$(SERVER_NAME)
DOCS_SERVER_IMAGE ?= $(REGISTRY_NAME)/$(PROJECT_NAMESPACE)/$(DOCS_SERVER_NAME)

CODE = notes_sync

all:
	@echo "make shell\t\t — activate shell"
	@echo "make format\t\t — reformat code with isort and black"

shell:
	poetry shell

format:
	poetry run isort $(CODE) $(if $(CHECK_ONLY),--check-only)
	poetry run black $(CODE) -t py311 $(if $(CHECK_ONLY),--check --diff)

run:
	poetry run python3 -m $(CODE)

db:
	docker compose -f docker-compose.yml up --detach --remove-orphans

open_db:
	docker exec -it notes_sync_db psql -U ${DB_USER} -W ${DB_NAME}

clean_db:
	docker compose down && docker volume rm $(shell docker volume ls --quiet)
