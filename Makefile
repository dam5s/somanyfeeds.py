.PHONY: check container dev-backend dev-frontend

check:
	uv run mypy backend tests
	uv run -m unittest
	cd frontend; npm test

container:
	docker build -f deployments/Dockerfile -t somanyfeeds-py .

dev-backend:
	RELOAD=true uv run -m backend.apps.api_server

dev-frontend:
	cd frontend; npm run dev
