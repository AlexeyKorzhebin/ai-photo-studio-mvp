APP_PORT ?= 8088

.PHONY: dev test lint build up down init-db frontend-build

dev:
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port $(APP_PORT)

test:
	pytest backend/tests

lint:
	python -m py_compile backend/app/main.py

build:
	cd frontend && npm run build

frontend-build:
	cd frontend && npm run build

up:
	docker compose -f infra/docker/docker-compose.yml up --build

down:
	docker compose -f infra/docker/docker-compose.yml down

init-db:
	python -m backend.app.db.init_db
