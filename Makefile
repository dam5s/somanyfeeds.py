.PHONY: check fix container dev-backend dev-frontend

check:
	uv sync --frozen
	uv run mypy backend backend_tests
	uv run ruff check
	uv run ruff format --check
	uv run -m unittest
	cd frontend && npm run lint && npm test

fix:
	uv run ruff check --fix
	uv run ruff format

container:
	docker build -f deployments/Dockerfile -t somanyfeeds-py .

dev:
	RELOAD=true uv run -m backend.apps.api_server &
	cd frontend; npm run dev
