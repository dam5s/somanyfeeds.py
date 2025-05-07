# We assume this is run from the top level of the repository

from node:22 as frontend_builder

workdir /frontend_build
copy package*.json ./
copy frontend/ .
run npm ci
run npm run build


from ghcr.io/astral-sh/uv:debian as uv_builder

workdir /uv_build
copy pyproject.toml uv.lock /uv_build/
run uv sync --frozen --no-dev
run uv pip compile pyproject.toml -o requirements.txt


from python:3.13-bookworm

workdir /app
copy --from=frontend_builder /frontend_build/dist/ /app/frontend/
copy --from=uv_builder /uv_build/requirements.txt /app/
copy backend/ /app/backend/
copy deployments/config /app
run pip install -r requirements.txt
run apt-get update && apt-get install -y nginx
run chmod u+x start.sh

expose 8080
cmd ["/app/start.sh"]
