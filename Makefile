.PHONY: up down check fix container db_migrate dev

up:
	docker compose up -d

down:
	docker compose down

check:
	uv sync --frozen
	uv run pyrefly check
	uv run ruff check
	uv run ruff format --check
	uv run -m unittest
	cd frontend && npm run check

fix:
	uv run ruff check --fix
	uv run ruff format
	cd frontend && npm run fix

container:
	docker build -f deployments/Dockerfile -t somanyfeeds-py .

db_migrate:
	cd databases/somanyfeeds_db; DATABASE_URL=postgresql://postgres:secret@localhost/somanyfeeds_dev uv run alembic upgrade head
	cd databases/somanyfeeds_db; DATABASE_URL=postgresql://postgres:secret@localhost/somanyfeeds_test uv run alembic upgrade head

dev:
	RELOAD=true uv run -m backend.apps.api_server &
	cd frontend; npm run dev
