.PHONY: check container

check:
	uv run mypy apps pkgs

container:
	docker build -f deployments/Dockerfile -t somanyfeeds-py .
