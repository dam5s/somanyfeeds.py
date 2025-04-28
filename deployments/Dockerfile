# We assume this is run from the top level of the repository

from node:22 as frontend_builder

workdir /frontend_build
copy package*.json ./
copy apps/browser_app ./browser_app
run npm ci
workdir /frontend_build/browser_app
run npm run build


from ghcr.io/astral-sh/uv:debian as uv_builder

workdir /uv_build
copy pyproject.toml uv.lock /uv_build/
run uv sync
run uv pip compile pyproject.toml -o requirements.txt


from python:3.13-bookworm

workdir /app
copy --from=frontend_builder /frontend_build/browser_app/dist/ /app/frontend/
copy --from=uv_builder /uv_build/requirements.txt /app/backend/
copy apps /app/backend/apps
copy pkgs /app/backend/pkgs
copy deployments/config /app
run chmod u+x start.sh

workdir /app/backend
run pip install -r requirements.txt

workdir /app
run apt-get update && apt-get install -y nginx

expose 8080
cmd ["/app/start.sh"]
